import os
import SimpleITK as sitk
import numpy as np
import scipy
import scipy.ndimage
import scipy.signal
import skimage.transform
import scipy.interpolate
import nibabel as nib
import nilearn
import matplotlib.pyplot as plt


def im2double(im):
    """
    Convert image from uint8 to double
    :param im: image uint8
    :return: image double
    """
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('uint8') - min_val) / (max_val - min_val)
    return out


def make_isotropic_sp(image, steps, res, is_label=False):
    """
    Resample an image to isotropic pixels (using smallest spacing from original) and save to file.
    Scipy/Numpy version
    :param image:
    :param steps:
    :param res:
    :param is_label: boolean, True if image is label, False if it is not. Change the interpolation method
    :return: isotropic array
    """
    x, y, z = [steps[k] * np.arange(image.shape[k]) for k in range(3)]  # original grid
    if is_label:
        method = 'nearest'
    else:
        method = 'linear'

    f = scipy.interpolate.RegularGridInterpolator((x, y, z), image, method=method)  # interpolator

    dx, dy, dz = res, res, res  # new step sizes # settings['EVAL']['target_voxel_dimension']
    new_grid = np.mgrid[0:x[-1]:dx, 0:y[-1]:dy, 0:z[-1]:dz]  # new grid
    new_grid = np.moveaxis(new_grid, (0, 1, 2, 3), (3, 0, 1, 2))  # reorder axes for evaluation
    return f(new_grid)


def make_isotropic_nilearn(image, res, is_label=False):
    """
    Resample an image to isotropic pixels (using smallest spacing from original) and save to file.
    Nilearn version
    :param image: nibabel file
    :param res: min resolution of the image
    :param is_label: boolean, True if image is label, False if it is not. Change the interpolation method
    :return: isotropic nibabel file
    """
    target_affine = np.diag((res, res, res))
    if is_label is True:
        method = 'nearest'
    else:
        method = 'linear'
    img_res = nilearn.image.resample_img(img=image, target_affine=target_affine, interpolation=method)
    return img_res


def make_isotropic(image, is_label=False):
    """
    Resample an image to isotropic pixels (using smallest spacing from original) and save to file. Many file formats
    (jpg, png,...) expect the pixels to be isotropic. By default the function uses a linear interpolator. For
    label images one should use the sitkNearestNeighbor interpolator so as not to introduce non-existant labels.
    SimpleITK version
    """
    if is_label:
        interpolator = sitk.sitkNearestNeighbor
    else:
        interpolator = sitk.sitkBSpline

    original_spacing = image.GetSpacing()
    # Image is already isotropic, just return a copy.
    if all(spc == original_spacing[0] for spc in original_spacing):
        return sitk.Image(image)
    # Make image isotropic via resampling
    original_size = image.GetSize()
    min_spacing = min(original_spacing)
    new_spacing = [min_spacing] * image.GetDimension()
    new_size = [int(round(osz * ospc / min_spacing)) for osz, ospc in zip(original_size, original_spacing)]
    return sitk.Resample(image, new_size, sitk.Transform(), interpolator,
                         image.GetOrigin(), new_spacing, image.GetDirection(), 0,
                         image.GetPixelID())


def resample_img(itk_image, out_spacing, is_label=False):
    """
    Resample images to specified spacing with SimpleITK
    :param itk_image: ITK image to be resampled
    :param out_spacing: spacing of the resulting ITK image after resampling
    :param is_label: boolean, True if image is label, False if it is not. Change the interpolation method
    :return: resampled ITK image
    """
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkLinear)

    return resample.Execute(itk_image)


def apply_tfm_matrix(img_tgt_path, img_ref_path, tfm_path, is_inverse=False, is_label=False, is_def=False):
    """
    Apply .tfm SimpleITK transformation to a target image
    :param img_tgt_path: path of the target image, or target image
    :param img_ref_path: path of the reference image, or reference image
    :param tfm_path: path of the transformation matrix file, or transformation matrix file
    :param is_inverse: whether the transformation is inverse or not
    :param is_label: whether the array is a label or not
    :param is_def: whether the transformation is nonrigid or not
    :return: transformed SimpleITK image
    """
    # 2.x-and-3.x-compatible code
    try:
        basestring
    except NameError:
        basestring = str
    #

    if isinstance(tfm_path, basestring):
        tfm = sitk.ReadTransform(str(tfm_path))
    else:
        tfm = tfm_path

    print(is_inverse)
    if is_inverse:
        if is_def:
            tfm = get_inverse_deformation_field(tfm)
        else:
            tfm = tfm.GetInverse()
    if isinstance(img_tgt_path, basestring):
        img_tgt = sitk.ReadImage(str(img_tgt_path))
    else:
        img_tgt = img_tgt_path
    if isinstance(img_ref_path, basestring):
        img_ref = sitk.ReadImage(str(img_ref_path))
    else:
        img_ref = img_ref_path
    if is_label:
        interpolator = sitk.sitkNearestNeighbor
    else:
        interpolator = sitk.sitkBSpline
    img_tfmed = sitk.Resample(img_tgt, img_ref, tfm, interpolator)
    return img_tfmed


def get_inverse_deformation_field(deform_tfm):
    """
    Calculate the inverse deformation field with SimpleITK
    :param deform_tfm: file tfm to invert
    :return: inverted matrix
    """
    disp_field_filter = sitk.TransformToDisplacementFieldFilter()
    disp_field = disp_field_filter.Execute(deform_tfm)
    inv_displ_field_filter = sitk.InverseDisplacementFieldImageFilter()
    inv_displ_field = inv_displ_field_filter.Execute(disp_field)
    inv_deform_tfm = sitk.DisplacementFieldTransform(inv_displ_field)
    return inv_deform_tfm


def sitk2nparray(image):
    return image


def nparray2sitk(image):
    return image


def mutual_information(hgram):
    """
    Mutual information for joint histogram
    """
    # Convert bins counts to probability values
    pxy = hgram / float(np.sum(hgram))
    px = np.sum(pxy, axis=1)  # marginal for x over y
    py = np.sum(pxy, axis=0)  # marginal for y over x
    px_py = px[:, None] * py[None, :]  # Broadcast to multiply marginals
    # Now we can do the calculation using the pxy, px_py 2D arrays
    nzs = pxy > 0  # Only non-zero pxy values contribute to the sum
    return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))


def downsampling_crosscorr(img1, img2, res):
    """
    Calculate correlation between two images at res levels of resolution
    :param img1: first image numpy array
    :param img2: second image numpy array
    :param res: list of downsampling rates
    :return: dictionary of variables at indicated resolution of correlation metric
    """

    corr_dict = {1: np.mean(scipy.signal.correlate(img1, img2, 'full'))}

    for i in res:
        if i > 1:
            i = i / 100
        corr_dict[i] = np.mean(scipy.signal.correlate(
            skimage.transform.rescale(img1, i, anti_aliasing=False, multichannel=False),
            skimage.transform.rescale(img2, i, anti_aliasing=False, multichannel=False), 'full'))

    return corr_dict


def downsampling_mi(img1, img2, res, n_bin):
    """
    Calculate mutual information between two images at res levels of resolution
    :param img1: first image numpy array
    :param img2: second image numpy array
    :param res: list of downsampling rates
    :param n_bin: number of bins of histogram
    :return: dictionary of variables at indicated resolution of cross correlation metric
    """

    hist_2d_100, x_edges_100, y_edges_100 = np.histogram2d(img1.ravel(), img2.ravel(), bins=n_bin)
    corr_dict = {1: mutual_information(hist_2d_100)}

    for i in res:
        if i > 1:
            i = i / 100
        hist_2d, x_edges, y_edges = np.histogram2d(
            skimage.transform.rescale(img1, i, anti_aliasing=False, multichannel=False).ravel(),
            skimage.transform.rescale(img2, i, anti_aliasing=False, multichannel=False).ravel(), bins=n_bin)
        corr_dict[i] = mutual_information(hist_2d)

    return corr_dict


def calculate_mae(im1_path, im2_path):
    """
    The mean absolute error (MAE) summarizes intensity differences between two images,
    with higher values indicating greater divergence.
    :param im1_path: first numpy array
    :param im2_path: second numpy array
    :return: RGB numpy array
    """
    im1_data = nib.load(str(im1_path)).get_data()
    im2_data = nib.load(str(im2_path)).get_data()
    abs_err = np.abs(im1_data - im2_data)
    mean_abs_err = np.mean(np.abs(im1_data - im2_data))
    # Get the color map by name
    cm = plt.get_cmap('seismic')
    # Apply the colormap like a function to greyscale array
    abs_err_colour_image = cm(abs_err)
    # print ('ABS err image', abs_err_colour_image.shape)
    # plt.imshow(abs_err_colour_image, cmap='seismic', vmin=-200, vmax=200)
    return abs_err, round(mean_abs_err, 3)


def intersection_of_union(im1, im2):
    """
    Intersection of the union (IOU) is a cost function.
    The IOU is the number of pixels filled in both images (the intersection) out of the number of pixels filled
    in either image (the union).
    :param im1: first image path
    :param im2: second image path
    :return: IOU float
    """
    im1_data = nib.load(str(im1)).get_data()
    im2_data = nib.load(str(im2)).get_data()
    i = np.logical_and(im1_data, im2_data)
    u = np.logical_or(im1_data, im2_data)

    return round(float(i.sum()) / float(u.sum()), 3)


def correct_header(img_list, img_ref_path):
    """
    Copy and broadcast a header from a reference image to one or more target images
    :param img_list: list of target images path
    :param img_ref_path: reference image path
    :return: None
    """
    reference_img = nib.load(str(img_ref_path))
    reference_header = reference_img.header

    for i in img_list:
        img_target = nib.load(str(i))
        out_path = os.path.dirname(str(i))
        name_target = os.path.basename(str(i))
        root_file = name_target.split('.')[0]
        x = nib.Nifti1Image(img_target.get_data(), reference_img.affine, reference_header)
        nib.save(x, os.path.join(out_path, str(root_file) + str('_hc.nii')))


# TODO aggiungere altri formati (mha, dicom?, nrrd?)
def read_image(img_path):
    img = nib.load(img_path)
    img_data = img.get_data()
    img_data = img_data.astype(np.float64)
    img_head = img.header
    return img_data, img_head, img


# TODO aggiungere altri formati (mha, dicom?, nrrd?)
def save_file(img_file, img_path):
    print("Type file: ", type(img_file))
    # TODO cambiare: non ragionare per img_path, ma per type di img_file
    if os.path.splitext(img_path)[1] in [".nii", ".nii.gz"]:
        print("File format: ", os.path.splitext(img_path)[1])
        sitk.WriteImage(img_file, str(img_path))
    elif os.path.splitext(img_path)[1] == ".tfm":
        print("File format: ", os.path.splitext(img_path)[1])
        sitk.WriteTransform(img_file, str(img_path))
    else:
        print("File format not yet supported")


def running_stats(filenames):
    """
    Calculates the running mean and stdev for a list of files using Welford's method.
    :param filenames: list of images
    :return: running mean and standard deviation
    """
    n = 0
    for filename in filenames:
        data, header, raw = read_image(filename)
        if n == 0:
            average = np.zeros_like(data)
            s = np.zeros_like(data)

        n += 1
        delta = data - average
        average += delta / n
        s += delta * (data - average)

    s /= n - 1
    np.sqrt(s, s)

    if n < 2:
        return average, None
    else:
        return average, s


def median_bins_fits(fitslist, B):
    mu, sigma = running_stats(fitslist)
    dim = mu.shape
    width = (2 * sigma) / B  # bin width
    left_bin = np.zeros(dim)  # counter for values < minval
    bins = np.zeros((dim[0], dim[1], dim[2], B))  # counter for bins

    for fitim in fitslist:
        data, header, raw = read_image(fitim)
        for i in range(dim[0]):
            for j in range(dim[1]):
                for k in range(dim[2]):
                    value = data[i, j, k]
                    mean = mu[i, j, k]
                    stdev = sigma[i, j, k]

                    if value < mean - stdev:
                        left_bin[i, j, k] += 1
                    elif mean + stdev > value >= mean - stdev:
                        bin_app = int((value - (mean - stdev)) / width[i, j, k])
                        # pezza per errore IndexError: index B is out of bounds for axis 3 with size B
                        # TODO capire cosa e
                        if bin_app >= bins.shape[3]:
                            break
                        bins[i, j, k, bin_app] += 1
                    # Values above maxval are ignored

    return mu, sigma, left_bin, bins


def median_approx_fits(fitslist, B):
    """
    Calculate
    :param fitslist: list of numpy array
    :param B: number of bins
    :return: median, mean and standard deviation numpy arrays
    """
    # Call median_bins to calculate the mean, std,
    # and bins for the input values
    mean, std, left_bin, bins = median_bins_fits(fitslist, B)
    dim = mean.shape
    # Position of the middle element
    N = len(fitslist)
    mid = (N + 1) / 2
    width = 2 * std / B

    # Calculate the approximated median for each array element
    median = np.zeros(dim)
    for i in range(dim[0]):
        for j in range(dim[1]):
            for k in range(dim[2]):
                count = left_bin[i, j, k]
                for b, bin_count in enumerate(bins[i, j, k]):
                    count += bin_count
                    if count >= mid:
                        # Stop when the cumulative count exceeds the midpoint
                        break
                median[i, j, k] = mean[i, j, k] - std[i, j, k] + width[i, j, k] * (b + 0.5)

    return median, mean, std
