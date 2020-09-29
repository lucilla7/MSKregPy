import numpy as np
import SimpleITK as sitk

from enum import Enum


# Use enumerations to represent the various evaluation measures
class OverlapMeasures(Enum):
    jaccard, dice, volume_similarity, false_negative, false_positive = range(5)


class SurfaceDistanceMeasures(Enum):
    hausdorff_distance, mean_surface_distance, median_surface_distance, std_surface_distance, max_surface_distance = \
        range(5)


def accuracy_calc(roi1, roi2):
    ref_path = roi1
    reference_segmentation = sitk.ReadImage(str(ref_path), sitk.sitkUInt8)

    segmentations_path = roi2
    segmentations = sitk.ReadImage(str(segmentations_path), sitk.sitkUInt8)

    # Empty numpy arrays to hold the results
    overlap_results = np.zeros(len(OverlapMeasures.__members__.items()))
    surface_distance_results = np.zeros(len(SurfaceDistanceMeasures.__members__.items()))

    # Compute the evaluation criteria

    # Note that for the overlap measures filter, because we are dealing with a single label we
    # use the combined, all labels, evaluation measures without passing a specific label to the methods.
    overlap_measures_filter = sitk.LabelOverlapMeasuresImageFilter()

    hausdorff_distance_filter = sitk.HausdorffDistanceImageFilter()

    # Use the absolute values of the distance map to compute the surface distances (distance map sign, outside or inside
    # relationship, is irrelevant)
    # label = 1
    reference_distance_map = sitk.Abs(sitk.SignedMaurerDistanceMap(reference_segmentation, squaredDistance=False))
    reference_surface = sitk.LabelContour(reference_segmentation)

    statistics_image_filter = sitk.StatisticsImageFilter()
    # Get the number of pixels in the reference surface by counting all pixels that are 1.
    statistics_image_filter.Execute(reference_surface)
    num_reference_surface_pixels = int(statistics_image_filter.GetSum())

    # Overlap measures
    overlap_measures_filter.Execute(reference_segmentation, segmentations)
    overlap_results[OverlapMeasures.jaccard.value] = overlap_measures_filter.GetJaccardCoefficient()
    overlap_results[OverlapMeasures.dice.value] = overlap_measures_filter.GetDiceCoefficient()
    overlap_results[OverlapMeasures.volume_similarity.value] = overlap_measures_filter.GetVolumeSimilarity()
    overlap_results[OverlapMeasures.false_negative.value] = overlap_measures_filter.GetFalseNegativeError()
    overlap_results[OverlapMeasures.false_positive.value] = overlap_measures_filter.GetFalsePositiveError()
    # Hausdorff distance
    hausdorff_distance_filter.Execute(reference_segmentation, segmentations)
    surface_distance_results[SurfaceDistanceMeasures.hausdorff_distance.value] = \
        hausdorff_distance_filter.GetHausdorffDistance()

    # Symmetric surface distance measures
    segmented_distance_map = sitk.Abs(sitk.SignedMaurerDistanceMap(segmentations, squaredDistance=False))
    segmented_surface = sitk.LabelContour(segmentations)

    # Multiply the binary surface segmentations with the distance maps. The resulting distance
    # maps contain non-zero values only on the surface (they can also contain zero on the surface)
    seg2ref_distance_map = reference_distance_map * sitk.Cast(segmented_surface, sitk.sitkFloat32)
    ref2seg_distance_map = segmented_distance_map * sitk.Cast(reference_surface, sitk.sitkFloat32)

    # Get the number of pixels in the segmented surface by counting all pixels that are 1.
    statistics_image_filter.Execute(segmented_surface)
    num_segmented_surface_pixels = int(statistics_image_filter.GetSum())

    # Get all non-zero distances and then add zero distances if required.
    seg2ref_distance_map_arr = sitk.GetArrayViewFromImage(seg2ref_distance_map)
    seg2ref_distances = list(seg2ref_distance_map_arr[seg2ref_distance_map_arr != 0])
    seg2ref_distances = seg2ref_distances + list(np.zeros(num_segmented_surface_pixels - len(seg2ref_distances)))
    ref2seg_distance_map_arr = sitk.GetArrayViewFromImage(ref2seg_distance_map)
    ref2seg_distances = list(ref2seg_distance_map_arr[ref2seg_distance_map_arr != 0])
    ref2seg_distances = ref2seg_distances + list(np.zeros(num_reference_surface_pixels - len(ref2seg_distances)))

    all_surface_distances = seg2ref_distances + ref2seg_distances

    surface_distance_results[SurfaceDistanceMeasures.mean_surface_distance.value] = np.mean(all_surface_distances)
    surface_distance_results[SurfaceDistanceMeasures.median_surface_distance.value] = np.median(all_surface_distances)
    surface_distance_results[SurfaceDistanceMeasures.std_surface_distance.value] = np.std(all_surface_distances)
    surface_distance_results[SurfaceDistanceMeasures.max_surface_distance.value] = np.max(all_surface_distances)

    return overlap_results, surface_distance_results
