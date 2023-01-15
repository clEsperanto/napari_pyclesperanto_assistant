import napari
import numpy as np
import pyclesperanto_prototype as cle
from napari_tools_menu import register_function

@register_function(menu="Measurement tables > Neighborhood statistics of measurements (clEsperanto)")
def neighborhood_statistics(labels_layer: napari.layers.Labels,
                            touching_neighbors:bool = True,
                            neighbors_of_touching_neighbors:bool = True,
                            proximal_neighbors:bool = False,
                            proximal_distance:float = 25,
                            n_nearest_neighbors:bool = False,
                            n:int = 6,
                            measure_mean_of_neighbors: bool = True,
                            measure_standard_deviation_of_neighbors: bool = True,
                            measure_minimum_of_neighbors: bool = False,
                            measure_maximum_of_neighbors: bool = False,
                            measure_median_of_neighbors: bool = False,
                            napari_viewer: napari.Viewer = None
                            ):
    """Takes a labels layer, reads out its feature table. Depending on which neighborhoods are specified
    and which `measure_*` parameters are set to True, it will compute e.g. the mean of touching neighbors and add a
    new column to the table. In this particular case, columns "mean_tn_[measure]" will be added.

    Parameters
    ----------
    labels_layer: napari.layers.Labels
        Napari labels layer
    touching_neighbors: bool, optional
        Touching neighbors will be considered for statistics
    neighbors_of_touching_neighbors: bool, optional
        touching neighbors of touching neighbors will be considered for statistics
    proximal_neighbors: bool, optional
        neighbors within a given distance will be considered for statistics
    proximal_distance: float, optional
        distance in pixels / voxels
    n_nearest_neighbors: bool, optional
        The n-nearest neighbors will be considered for statistics
    n: int, optional
        number of n-nearest neighbors. Note: n=1 is the cell itself.
    measure_mean_of_neighbors: bool, optional
        compute the mean of specified neighbors
    measure_standard_deviation_of_neighbors: bool, optional
        compute the standard deviation of specified neighbors
    measure_minimum_of_neighbors: bool, optional
        compute the minimum of specified neighbors
    measure_maximum_of_neighbors: bool, optional
        compute the maximum of specified neighbors
    measure_median_of_neighbors: bool, optional
        compute the median of specified neighbors
    napari_viewer: napari.Viewer, optional
        If the viewer is given, it will add this table to the graphical user interface of the viewer.
        Otherwise, it will return the table.

    """
    if hasattr(labels_layer, "features"):
        table = labels_layer.features
    else:
        table = labels_layer.properties

    table = neighborhood_statistics_of_data(
        labels_layer.data,
        table,
        touching_neighbors,
        neighbors_of_touching_neighbors,
        proximal_neighbors,
        proximal_distance,
        n_nearest_neighbors,
        n,
        measure_mean_of_neighbors,
        measure_standard_deviation_of_neighbors,
        measure_minimum_of_neighbors,
        measure_maximum_of_neighbors,
        measure_median_of_neighbors,
    )

    if napari_viewer is not None:
        # Store results in the properties dictionary:
        labels_layer.properties = table

        # turn table into a widget
        from napari_skimage_regionprops import add_table
        add_table(labels_layer, napari_viewer)
    else:
        return table


def neighborhood_statistics_of_data(
    label_image: napari.types.LabelsData,
    table:dict,
    touching_neighbors: bool = True,
    neighbors_of_touching_neighbors: bool = True,
    proximal_neighbors: bool = False,
    proximal_distance: float = 25,
    n_nearest_neighbors: bool = False,
    n:int=6,
    measure_mean_of_neighbors: bool = True,
    measure_standard_deviation_of_neighbors: bool = True,
    measure_minimum_of_neighbors: bool = False,
    measure_maximum_of_neighbors: bool = False,
    measure_median_of_neighbors: bool = False,
):
    """Takes a label image and a table with corresponding measurements. Depending on which neighborhoods are specified
    and which `measure_*` parameters are set to True, it will compute e.g. the mean of touching neighbors and add a
    new column to the table. In this particular case, columns "mean_tn_[measure]" will be added.
    """
    neighborhoods = {}

    if not np.array_equal(table['label'], range(1, len(table['label']) + 1)):
        raise ValueError("Measurements must contain a column 'label' which is sequentially ordered from 1 to n, for n labels.")

    if touching_neighbors or neighbors_of_touching_neighbors:

        # determine neighbors
        touch_matrix = cle.generate_touch_matrix(label_image)
        if touching_neighbors:
            neighborhoods["tn"] = touch_matrix

        if neighbors_of_touching_neighbors:
            # determine neighbors of neigbors
            neighbors_of_neighbors = cle.neighbors_of_neighbors(touch_matrix)
            neighborhoods["tntn"] = neighbors_of_neighbors[1:,1:] # ignore background (first row/column)

    if proximal_neighbors or n_nearest_neighbors:
        coordinates = cle.centroids_of_labels(label_image)
        distance_matrix = cle.generate_distance_matrix(coordinates, coordinates)
        if proximal_neighbors:
            proximal_neighbors_matrix = cle.generate_proximal_neighbors_matrix(distance_matrix, max_distance=proximal_distance)
            neighborhoods["pn" + str(proximal_distance)] = proximal_neighbors_matrix[1:,1:] # ignore background (first row/column)

        if n_nearest_neighbors:
            n_nearest_neighbors_matrix = cle.generate_n_nearest_neighbors_matrix(distance_matrix, n=n)
            neighborhoods["nn" + str(n)] = n_nearest_neighbors_matrix[1:,1:] # ignore background (first row/column)

    output_table = {}

    for key, element in table.items():
        output_table[key] = element
        if key.lower() in ["label", "frame", "index"]:
            continue

        if isinstance(element, (tuple, list)):
            element = np.asarray([element])

        if len(element.shape) == 1:
            element = np.asarray([element])

        for neighborhood_name, neighborhood in neighborhoods.items():
            if measure_mean_of_neighbors:
                mean = cle.mean_of_touching_neighbors(element, neighborhood)
                output_table["mean_" + neighborhood_name + "_" + key] = np.asarray(mean)[0].tolist()

            if measure_standard_deviation_of_neighbors:
                stddev = cle.standard_deviation_of_touching_neighbors(element, neighborhood)
                output_table["std_" + neighborhood_name + "_" + key] = np.asarray(stddev)[0].tolist()

            if measure_minimum_of_neighbors:
                minimum = cle.minimum_of_touching_neighbors(element, neighborhood)
                output_table["min_" + neighborhood_name + "_" + key] = np.asarray(minimum)[0].tolist()

            if measure_maximum_of_neighbors:
                maximum = cle.maximum_of_touching_neighbors(element, neighborhood)
                output_table["max_" + neighborhood_name + "_" + key] = np.asarray(maximum)[0].tolist()

            if measure_median_of_neighbors:
                median = cle.median_of_touching_neighbors(element, neighborhood)
                output_table["median_" + neighborhood_name + "_" + key] = np.asarray(median)[0].tolist()

    return output_table