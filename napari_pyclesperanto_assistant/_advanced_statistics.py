import warnings

import napari
import pyclesperanto_prototype as cle
from napari_tools_menu import register_function
import numpy as np

@register_function(menu="Measurement tables > Statistics of labeled pixels including neighborhood statistics (deprecated, clEsperanto)")
def advanced_statistics(
        intensity_image: napari.types.ImageData,
        label_image: napari.types.LabelsData,
        measure_intensity: bool = True,
        measure_shape: bool = True,
        measure_distance_to_n_nearest_neigbors: bool = True,
        n_neighbors: str = "2,3,4",
        napari_viewer: napari.Viewer = None
    ) -> "pandas.DataFrame":
    warnings.warn("'Statistics of labeled pixels including neighborhood statistics' is deprecated. Use 'Label statistics' instead.")

    n_neighbors_list = map(int, n_neighbors.split(","))

    # select columns, depending on if intensities and/or shape were selected
    columns = ["label", "centroid_x", "centroid_y", "centroid_z"]

    if measure_intensity:
        columns = columns + [
            "min_intensity",
            "max_intensity",
            "sum_intensity",
            "mean_intensity",
            "standard_deviation_intensity",
        ]

    if measure_shape:
        columns = columns + [
            "area",
            "mean_distance_to_centroid",
            "max_distance_to_centroid",
            "mean_max_distance_to_centroid_ratio",
        ]

    # Determine Region properties using clEsperanto
    region_props = cle.statistics_of_labelled_pixels(intensity_image, label_image)

    if not measure_distance_to_n_nearest_neigbors:
        table = {
            column: value for column, value in region_props.items() if column in columns
        }
    else:
        table = region_props_with_neighborhood_data(
            columns, label_image, n_neighbors_list, region_props
        )

    if napari_viewer is not None:
        # Store results in the properties dictionary:
        from napari_workflows._workflow import _get_layer_from_data
        labels_layer = _get_layer_from_data(napari_viewer, label_image)
        labels_layer.properties = table

        # turn table into a widget
        from napari_skimage_regionprops import add_table
        add_table(labels_layer, napari_viewer)
    else:
        import pandas
        return pandas.DataFrame(table)


def region_props_with_neighborhood_data(
    columns, label_image, n_neighbors_list, region_props
):
    """
    Calculate neighborhood regionproperties and combine with other regionproperties

    Parameters
    ----------
    columns: list
        list of names of regionproperties
    label_image : numpy array
        segmented image with background = 0 and labels >= 1
    region_props: dict
        region properties to be combined with
    n_closest_points_list: list
        number of closest neighbors for which neighborhood properties will be calculated
    """
    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(label_image)

    # ignore touching the background
    cle.set_column(touch_matrix, 0, 0)
    cle.set_row(touch_matrix, 0, 0)

    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(label_image)

    # generate a distance matrix
    distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)

    # determine touching neighbor count
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(touching_neighbor_count, 0, 0)

    # iterating over different neighbor numbers for average neighbor distance calculation
    for i in n_neighbors_list:
        distance_of_n_closest_points = cle.pull(
            cle.average_distance_of_n_closest_points(cle.push(distance_matrix), n=i)
        )[0]

        # addition to the regionprops dictionary
        region_props[
            f"avg_distance_of_{i}_nearest_neigbors"
        ] = distance_of_n_closest_points[1:]

    # processing touching neighbor count for addition to regionprops (deletion of background)
    touching_neighbor_c = cle.pull(touching_neighbor_count)[0,1:]

    # addition to the regionprops dictionary
    region_props["touching_neighbor_count"] = touching_neighbor_c
    print("Measurements Completed.")

    return region_props

from napari_skimage_regionprops._all_frames import analyze_all_frames

regionprops_table_all_frames = analyze_all_frames(advanced_statistics)
register_function(regionprops_table_all_frames, menu="Measurement tables > Statistics of labeled pixels including neighborhood statistics of all frames (clEsperanto)")
