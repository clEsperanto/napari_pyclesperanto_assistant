
def advanced_statistics():
    
    n_neighbors_list = map(int, n_neighbors_str.split(","))

def get_regprops_from_regprops_source(
    intensity_image, label_image, region_props_source, n_closest_points_list=[2, 3, 4]
):
    """
    Calculate Region properties based on the region properties source string

    Parameters
    ----------
    intensity_image : numpy array
        original image from which the labels were generated
    label_image : numpy array
        segmented image with background = 0 and labels >= 1
    region_props_source: str
        must include either shape, intensity, both or neighborhood
    n_closest_points_list: list
        number of closest neighbors for which neighborhood properties will be calculated
    """
    # and select columns, depending on if intensities and/or shape were selected
    columns = ["label", "centroid_x", "centroid_y", "centroid_z"]

    if "intensity" in region_props_source:
        columns = columns + [
            "min_intensity",
            "max_intensity",
            "sum_intensity",
            "mean_intensity",
            "standard_deviation_intensity",
        ]

    if "shape" in region_props_source:
        columns = columns + [
            "area",
            "mean_distance_to_centroid",
            "max_distance_to_centroid",
            "mean_max_distance_to_centroid_ratio",
        ]

    # Determine Region properties using clEsperanto
    reg_props = cle.statistics_of_labelled_pixels(intensity_image, label_image)

    if "shape" in region_props_source or "intensity" in region_props_source:
        return {
            column: value for column, value in reg_props.items() if column in columns
        }

    if "neighborhood" in region_props_source:
        return region_props_with_neighborhood_data(
            columns, label_image, n_closest_points_list, reg_props
        )


def region_props_with_neighborhood_data(
    columns, label_image, n_closest_points_list, reg_props
):
    """
    Calculate neighborhood regionproperties and combine with other regionproperties

    Parameters
    ----------
    columns: list
        list of names of regionproperties
    label_image : numpy array
        segmented image with background = 0 and labels >= 1
    reg_props: dict
        region properties to be combined with
    n_closest_points_list: list
        number of closest neighbors for which neighborhood properties will be calculated
    """
    if isinstance(label_image, da.core.Array):
        label_image = np.asarray(label_image)
    # get the lowest label index to adjust sizes of measurement arrays
    min_label = int(np.min(label_image[np.nonzero(label_image)]))

    columns = columns + [
        "min_intensity",
        "max_intensity",
        "sum_intensity",
        "mean_intensity",
        "standard_deviation_intensity",
        "area",
        "mean_distance_to_centroid",
        "max_distance_to_centroid",
        "mean_max_distance_to_centroid_ratio",
    ]

    region_props = {
        column: value for column, value in reg_props.items() if column in columns
    }

    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(label_image)

    # ignore touching the background
    cle.set_column(touch_matrix, 0, 0)
    cle.set_row(touch_matrix, 0, 0)

    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(label_image)

    # generate a distance matrix
    distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)

    # detect touching neighbor count
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(touching_neighbor_count, 0, 0)

    # conversion and editing of the distance matrix, so that it does not break cle.average_distance
    view_dist_mat = cle.pull(distance_matrix)
    temp_dist_mat = np.delete(view_dist_mat, range(min_label), axis=0)
    edited_dist_mat = np.delete(temp_dist_mat, range(min_label), axis=1)

    # iterating over different neighbor numbers for average neighbor distance calculation
    for i in n_closest_points_list:
        distance_of_n_closest_points = cle.pull(
            cle.average_distance_of_n_closest_points(cle.push(edited_dist_mat), n=i)
        )[0]

        # addition to the regionprops dictionary
        region_props[
            f"avg distance of {i} closest points"
        ] = distance_of_n_closest_points

    # processing touching neighbor count for addition to regionprops (deletion of background & not used labels)
    touching_neighbor_c = cle.pull(touching_neighbor_count)
    touching_neighbor_count_formatted = np.delete(
        touching_neighbor_c, list(range(min_label))
    )

    # addition to the regionprops dictionary
    region_props["touching neighbor count"] = touching_neighbor_count_formatted
    print("Measurements Completed.")

    return region_props
