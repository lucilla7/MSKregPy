# MSKregPy
MSKregPy is a collection of algorithms and GUI for muscolo-skeletal image processing and registration.

wxPython library was employed to develop the GUI, which is composed by two main windows – initial window and registration window – and 5 secondary frames for support functionalities. 
3D images are presented with three views – axial, coronal and sagittal – with three sliders to adjust maximum value, minimum value, and gamma correction. 

On the topmost part of the registration window, users may choose to apply a mask to either or both the fixed and the moving image, and to make the image voxels isotropic. 

The framework also allows the concatenation of three different types of 3D transformations, a rototraslation, an affine and a FFD b-spline elastic transformation. It is possible to choose the type (Mean Squares, Cross-Correlation and Mattes Mutual Information) and the sampling rate for the metric; the learning rate, the iterations number, the convergence minimum value and the window size for the gradient descent optimizer, the shrink factors and the smoothing sigmas for the multi-resolution approach, and finally the 3D mesh size for the elastic transformation only. 

The progress and the products of the registration – fixed image, registered image and metric evolution – are shown in two separate windows, raised only after the registration process is started. 

The menu bar of the initial window contains the <i>Image Proc</i> element, dedicated to these functions: 
<ul>
<li><i>Apply tfm</i> window: given an initial target image, allows to concatenate up to four SimpleITK  tfm transformations, with the option to apply the inverse of the transformation. 
</li>
<li><i>Stat Calculator</i> window: Calculates the running median using the binapprox method (<a href="https://arxiv.org/abs/0806.3301">Tibshirani 2008</a>), running mean and standard deviation (<a href="https://amstat.tandfonline.com/doi/abs/10.1080/00401706.1962.10490022">Welford 1962</a>), and shows and saves the results in the same folder of the reference image(s). The input can be a directory containing the images of interest, or a 4D file. 
</li>
<li><i>Copy Header</i> window: after loading a reference image, broadcasts the header to a list of corrupted images.
</li>

For questions, requesting assistance, suggesting enhancements or new ideas as well as for reporting bugs, please open an <a href="https://github.com/lucilla7/MSKregPy/issues">issue</a> to contact us.
