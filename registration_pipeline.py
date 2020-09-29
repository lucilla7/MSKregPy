import time
import SimpleITK as sitk
import utility_fx
import reg_process

metric_values = []
multires_iterations = []
registration_progress = []


def store_values(registration_method):
    global metric_values, multires_iterations
    metric_values.append(registration_method.GetMetricValue())
    return metric_values


def update_multires_iterations():
    global metric_values, multires_iterations
    print("Multires Iteration")
    print(len(multires_iterations))
    multires_iterations.append(len(metric_values))
    return multires_iterations


def make_registration(fixed_img_path, moving_img_path, fixed_msk_path, moving_msk_path, iso_img, tfm_dict):
    global metric_values, multires_iterations, registration_progress
    pixelType = sitk.sitkFloat32
    # pixel_type_label = sitk.sitkUInt8
    fixed_img_in = sitk.ReadImage(str(fixed_img_path), pixelType)
    moving_img_in = sitk.ReadImage(str(moving_img_path), pixelType)
    maskFixed = None
    maskMoving = None

    regim_list = dict(rigid=None, elastic=None, affine=None)
    regtfm_list = dict(rigid=None, elastic=None, affine=None)

    if fixed_msk_path is not None:
        maskFixed = sitk.ReadImage(str(fixed_msk_path), sitk.sitkUInt8)
    if moving_msk_path is not None:
        maskMoving = sitk.ReadImage(str(moving_msk_path), sitk.sitkUInt8)

    # if iso_img is True make images and eventual masks isotropic
    if iso_img:
        fixed_img = utility_fx.make_isotropic(fixed_img_in)
        moving_img = utility_fx.make_isotropic(moving_img_in)
        if maskFixed is not None:
            maskFixed = utility_fx.make_isotropic(maskFixed, is_label=True)

        if maskMoving is not None:
            maskMoving = utility_fx.make_isotropic(maskMoving, is_label=True)

    else:
        fixed_img = fixed_img_in
        moving_img = moving_img_in

    # calculating time elapsed
    start_time = time.time()

    # open registration progress window
    reg_progress_win = reg_process.RegistrationProcess(parent=None)
    reg_progress_win.Show()

    # rigid transform
    if tfm_dict['rigid'] is not None:
        initial_transform = sitk.CenteredTransformInitializer(fixed_img,
                                                              moving_img,
                                                              sitk.Euler3DTransform(),
                                                              sitk.CenteredTransformInitializerFilter.MOMENTS)

        # reg_progress_win.reg_gauge.Pulse()

        registration_method_rigid = sitk.ImageRegistrationMethod()

        # set sampling metric
        if tfm_dict['rigid']['metric']['name'] == 'Mean Squares':
            registration_method_rigid.SetMetricAsMeanSquares()
        elif tfm_dict['rigid']['metric']['name'] == 'Correlation':
            registration_method_rigid.SetMetricAsCorrelation()
        elif tfm_dict['rigid']['metric']['name'] == 'Mattes MI':
            registration_method_rigid.SetMetricAsMattesMutualInformation()
        registration_method_rigid.SetMetricSamplingStrategy(registration_method_rigid.RANDOM)
        registration_method_rigid.SetMetricSamplingPercentage(tfm_dict['rigid']['metric']['s_perc'])
        registration_method_rigid.SetInterpolator(sitk.sitkLinear)

        # if masks are not empty, set them to select the area for metric calculation
        if maskFixed is not None:
            registration_method_rigid.SetMetricFixedMask(maskFixed)
        if maskMoving is not None:
            registration_method_rigid.SetMetricMovingMask(maskMoving)

        # set optimizer
        registration_method_rigid.SetOptimizerAsGradientDescent(learningRate=
                                                                tfm_dict['rigid']['optimizers']['learning_rate'],
                                                                numberOfIterations=
                                                                tfm_dict['rigid']['optimizers']['iterations'],
                                                                estimateLearningRate=0,
                                                                convergenceMinimumValue=
                                                                float('1e-' + str(
                                                                    tfm_dict['rigid']['optimizers']['minval'])),
                                                                convergenceWindowSize=
                                                                tfm_dict['rigid']['optimizers']['window_size'])

        registration_method_rigid.SetOptimizerScalesFromPhysicalShift()

        # Setup for the multi-resolution framework. 3 steps are optimal
        registration_method_rigid.SetShrinkFactorsPerLevel(tfm_dict['rigid']['multires']['shrinking_factors'])
        registration_method_rigid.SetSmoothingSigmasPerLevel(tfm_dict['rigid']['multires']['smoothing_sigmas'])
        registration_method_rigid.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        registration_method_rigid.SetInitialTransform(initial_transform, inPlace=False)

        reg_progress_win.update_list(listprog="Rigid Transform")
        reg_progress_win.update_list(listprog="-------")
        reg_progress_win.update_list(listprog=str(initial_transform))

        # events
        registration_method_rigid.AddCommand(sitk.sitkIterationEvent,
                                             lambda: store_values(registration_method_rigid))
        registration_method_rigid.AddCommand(sitk.sitkIterationEvent,
                                             lambda: reg_progress_win.update_list("Iteration: " +
                                                                                  str(len(metric_values)) + " Metric: "
                                                                                  + str(registration_method_rigid.
                                                                                        GetMetricValue())))
        registration_method_rigid.AddCommand(sitk.sitkMultiResolutionIterationEvent,
                                             lambda: update_multires_iterations())

        outTx_rigid = registration_method_rigid.Execute(fixed_img, moving_img)
        # reg_progress_win.reg_gauge.Pulse()
        moving_resampled = sitk.Resample(moving_img, fixed_img, outTx_rigid, sitk.sitkBSpline, 0.0,
                                         moving_img.GetPixelID())

        rigid_time = time.time() - start_time

        reg_progress_win.update_list(listprog="-------")
        reg_progress_win.update_list(listprog=str(outTx_rigid))
        reg_progress_win.update_list(listprog=" Optimizer stop condition: {0} ".format(
            registration_method_rigid.GetOptimizerStopConditionDescription()))
        reg_progress_win.update_list(
            listprog=" Iteration: {0}".format(registration_method_rigid.GetOptimizerIteration()))
        reg_progress_win.update_list(
            listprog=" Metric value: {0}".format(registration_method_rigid.GetMetricValue()))
        reg_progress_win.update_list(listprog=str("Time elapsed: " + str(rigid_time)))
        # reg_progress_win.reg_gauge.Pulse()

        if maskMoving is not None:
            maskMoving = sitk.Resample(maskMoving, fixed_img, outTx_rigid, sitk.sitkNearestNeighbor, 0.0,
                                       moving_img.GetPixelID())

        moving_img = moving_resampled
        if tfm_dict['affine'] is None and tfm_dict['elastic'] is None:
            regim_list['rigid'] = utility_fx.resample_img(moving_resampled, fixed_img_in.GetSpacing())
        else:
            regim_list['rigid'] = moving_resampled
        regtfm_list['rigid'] = outTx_rigid

    if tfm_dict['affine'] is not None:
        initial_transform = sitk.CenteredTransformInitializer(fixed_img,
                                                              moving_img,
                                                              sitk.AffineTransform(3),
                                                              sitk.CenteredTransformInitializerFilter.MOMENTS)

        # reg_progress_win.reg_gauge.Pulse()

        registration_method_affine = sitk.ImageRegistrationMethod()
        if tfm_dict['affine']['metric']['name'] == 'Mean Squares':
            registration_method_affine.SetMetricAsMeanSquares()
        elif tfm_dict['affine']['metric']['name'] == 'Correlation':
            registration_method_affine.SetMetricAsCorrelation()
        elif tfm_dict['affine']['metric']['name'] == 'Mattes MI':
            registration_method_affine.SetMetricAsMattesMutualInformation()
        registration_method_affine.SetMetricSamplingStrategy(registration_method_affine.RANDOM)
        registration_method_affine.SetMetricSamplingPercentage(tfm_dict['affine']['metric']['s_perc'])
        registration_method_affine.SetInterpolator(sitk.sitkLinear)

        # if masks are not empty, set them to select the area for metric calculation
        if maskFixed is not None:
            registration_method_affine.SetMetricFixedMask(maskFixed)
        if maskMoving is not None:
            registration_method_affine.SetMetricMovingMask(maskMoving)

        # set optimizer
        registration_method_affine.SetOptimizerAsGradientDescent(learningRate=
                                                                 tfm_dict['affine']['optimizers']['learning_rate'],
                                                                 numberOfIterations=
                                                                 tfm_dict['affine']['optimizers']['iterations'],
                                                                 estimateLearningRate=0,
                                                                 convergenceMinimumValue=
                                                                 float('1e-' + str(
                                                                     tfm_dict['affine']['optimizers']['minval'])),
                                                                 convergenceWindowSize=
                                                                 tfm_dict['affine']['optimizers']['window_size'])

        registration_method_affine.SetOptimizerScalesFromPhysicalShift()

        # Setup for the multi-resolution framework. 3 steps are optimal
        registration_method_affine.SetShrinkFactorsPerLevel(tfm_dict['affine']['multires']['shrinking_factors'])
        registration_method_affine.SetSmoothingSigmasPerLevel(tfm_dict['affine']['multires']['smoothing_sigmas'])
        registration_method_affine.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        registration_method_affine.SetInitialTransform(initial_transform, inPlace=False)

        reg_progress_win.update_list(listprog="Affine Transform")
        reg_progress_win.update_list(listprog="-------")
        reg_progress_win.update_list(listprog=str(initial_transform))

        # events
        registration_method_affine.AddCommand(sitk.sitkIterationEvent,
                                              lambda: store_values(registration_method_affine))
        registration_method_affine.AddCommand(sitk.sitkIterationEvent,
                                              lambda: reg_progress_win.update_list("Iteration: " +
                                                                                   str(len(metric_values)) + " Metric: "
                                                                                   + str(registration_method_affine.
                                                                                         GetMetricValue())))
        registration_method_affine.AddCommand(sitk.sitkMultiResolutionIterationEvent,
                                              lambda: update_multires_iterations())

        outTx_affine = registration_method_affine.Execute(fixed_img, moving_img)
        # reg_progress_win.reg_gauge.Pulse()
        moving_resampled = sitk.Resample(moving_img, fixed_img, outTx_affine, sitk.sitkBSpline, 0.0,
                                         moving_img.GetPixelID())

        affine_time = time.time() - start_time

        reg_progress_win.update_list(listprog="-------")
        reg_progress_win.update_list(listprog=str(outTx_affine))
        reg_progress_win.update_list(listprog=" Optimizer stop condition: {0} ".format(
            registration_method_affine.GetOptimizerStopConditionDescription()))
        reg_progress_win.update_list(
            listprog=" Iteration: {0}".format(registration_method_affine.GetOptimizerIteration()))
        reg_progress_win.update_list(
            listprog=" Metric value: {0}".format(registration_method_affine.GetMetricValue()))
        reg_progress_win.update_list(listprog=str("Time elapsed: " + str(affine_time)))
        # reg_progress_win.reg_gauge.Pulse()

        if maskMoving is not None:
            maskMoving = sitk.Resample(maskMoving, fixed_img, outTx_affine, sitk.sitkNearestNeighbor, 0.0,
                                       moving_img.GetPixelID())

        moving_img = moving_resampled
        if tfm_dict['elastic'] is None:
            regim_list['affine'] = utility_fx.resample_img(moving_resampled, fixed_img_in.GetSpacing())
        else:
            regim_list['affine'] = moving_resampled
        regtfm_list['affine'] = outTx_affine

    if tfm_dict['elastic'] is not None:

        # Determine the number of BSpline control points using the physical
        # spacing we want for the finest resolution control grid.
        transformDomainMeshSize = tfm_dict['elastic']['mesh_size']
        tx = sitk.BSplineTransformInitializer(fixed_img,
                                              transformDomainMeshSize)

        reg_progress_win.update_list(listprog="Elastic Transform")
        reg_progress_win.update_list(listprog="-------")
        reg_progress_win.update_list(listprog=str(tx))

        registration_method_elastic = sitk.ImageRegistrationMethod()
        registration_method_elastic.SetInitialTransformAsBSpline(tx, inPlace=False)

        # Similarity metric settings.
        if tfm_dict['elastic']['metric']['name'] == 'Mean Squares':
            registration_method_elastic.SetMetricAsMeanSquares()
        elif tfm_dict['elastic']['metric']['name'] == 'Correlation':
            registration_method_elastic.SetMetricAsCorrelation()
        elif tfm_dict['elastic']['metric']['name'] == 'Mattes MI':
            registration_method_elastic.SetMetricAsMattesMutualInformation()
        registration_method_elastic.SetMetricSamplingStrategy(registration_method_elastic.RANDOM)
        registration_method_elastic.SetMetricSamplingPercentage(tfm_dict['elastic']['metric']['s_perc'])

        if maskFixed is not None:
            registration_method_elastic.SetMetricFixedMask(maskFixed)
        if maskMoving is not None:
            registration_method_elastic.SetMetricMovingMask(maskMoving)
        registration_method_elastic.SetInterpolator(sitk.sitkLinear)

        # Optimizer settings.
        registration_method_elastic.SetOptimizerAsGradientDescentLineSearch(learningRate=
                                                                            tfm_dict['elastic']['optimizers'][
                                                                                'learning_rate'],
                                                                            numberOfIterations=
                                                                            tfm_dict['elastic']['optimizers'][
                                                                                'iterations'],
                                                                            convergenceMinimumValue=
                                                                            float('1e-' + str(
                                                                                tfm_dict['elastic']['optimizers'][
                                                                                    'minval'])),
                                                                            convergenceWindowSize=
                                                                            tfm_dict['elastic']['optimizers'][
                                                                                'window_size'])

        registration_method_elastic.SetOptimizerScalesFromPhysicalShift()

        # Setup for the multi-resolution framework
        registration_method_elastic.SetShrinkFactorsPerLevel(tfm_dict['elastic']['multires']['shrinking_factors'])
        registration_method_elastic.SetSmoothingSigmasPerLevel(tfm_dict['elastic']['multires']['smoothing_sigmas'])
        registration_method_elastic.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        # events
        registration_method_elastic.AddCommand(sitk.sitkIterationEvent,
                                               lambda: store_values(registration_method_elastic))
        registration_method_elastic.AddCommand(sitk.sitkIterationEvent,
                                               lambda: reg_progress_win.update_list("Iteration: " +
                                                                                    str(len(
                                                                                        metric_values)) + " Metric: "
                                                                                    + str(registration_method_elastic.
                                                                                          GetMetricValue())))
        registration_method_elastic.AddCommand(sitk.sitkMultiResolutionIterationEvent,
                                               lambda: update_multires_iterations())

        outTx_elastic = registration_method_elastic.Execute(fixed_img, moving_img)

        elastic_time = time.time() - start_time

        reg_progress_win.update_list(listprog="-------")
        reg_progress_win.update_list(listprog=str(outTx_elastic))
        reg_progress_win.update_list(listprog=" Optimizer stop condition: {0} ".format(
            registration_method_elastic.GetOptimizerStopConditionDescription()))
        reg_progress_win.update_list(
            listprog=" Iteration: {0}".format(registration_method_elastic.GetOptimizerIteration()))
        reg_progress_win.update_list(
            listprog=" Metric value: {0}".format(registration_method_elastic.GetMetricValue()))
        reg_progress_win.update_list(listprog=str("Time elapsed: " + str(elastic_time)))

        moving_resampled = sitk.Resample(moving_img, fixed_img, outTx_elastic, sitk.sitkBSpline,
                                         0.0, moving_img.GetPixelID())

        regim_list['elastic'] = utility_fx.resample_img(moving_resampled, fixed_img_in.GetSpacing())
        regtfm_list['elastic'] = outTx_elastic

    reg_tuples = (regim_list, regtfm_list), (metric_values, multires_iterations)
    del metric_values
    del multires_iterations
    del registration_progress

    return reg_tuples
