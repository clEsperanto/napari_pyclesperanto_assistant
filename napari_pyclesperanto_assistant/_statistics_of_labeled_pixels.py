import warnings
import napari
import pyclesperanto_prototype as cle
from napari_skimage_regionprops._all_frames import analyze_all_frames
from napari_tools_menu import register_function

@register_function(menu="Measurement > Label statistics (clEsperanto)")
def label_statistics(image: "napari.types.ImageData",
                                 labels: "napari.types.LabelsData",
                                 intensity:bool = True,
                                 size:bool = True,
                                 shape:bool = False,
                                 position:bool = False,
                                 neighbors:bool = False,
                                 napari_viewer : "napari.Viewer"=None) -> "pandas.DataFrame":
    """
    Adds a table widget to a given napari viewer with quantitative analysis results derived from an image-label-image pair.
    """
    if image is not None and labels is not None:
        import pandas as pd

        table = {}
        if intensity or size or shape or position:
            result = cle.statistics_of_labelled_pixels(image, labels)
            copy_keys(result, table, ['label'])
            if intensity:
                copy_keys(result, table, ['min_intensity', 'max_intensity', 'mean_intensity',
                                          'sum_intensity', 'standard_deviation_intensity'])
            if position:
                copy_keys(result, table, ['centroid_x', 'centroid_y', 'centroid_z',
                                          'mass_center_x', 'mass_center_y', 'mass_center_z',
                                          'bbox_max_x', 'bbox_max_y', 'bbox_max_z'])
            if size:
                copy_keys(result, table, ['bbox_width', 'bbox_height', 'bbox_depth'])
                if 'pixel_count' in result.keys():
                    copy_keys(result, table, ['pixel_count'])
                else:
                    table['pixel_count'] = result['area']
            if shape:
                copy_keys(result, table, ['mean_max_distance_to_mass_center_ratio',
                                          'mean_max_distance_to_centroid_ratio'])
        if neighbors:
            result = cle.statistics_of_labelled_neighbors(label_image=labels)
            if len(table.keys()) > 0:
                df1 = pd.DataFrame(result)
                df2 = pd.DataFrame(table)
                df3 = pd.merge(df1, df2, how='inner', on='label')
                table = df3.to_dict(orient='list')
            else:
                table = result


        if napari_viewer is not None:
            # Store results in the properties dictionary:
            from napari_workflows._workflow import _get_layer_from_data
            labels_layer = _get_layer_from_data(napari_viewer, labels)
            labels_layer.properties = table

            # turn table into a widget
            from napari_skimage_regionprops import add_table
            add_table(labels_layer, napari_viewer)
        else:
            return pd.DataFrame(table)
    else:
        warnings.warn("Image and labels must be set.")

regionprops_table_all_frames = analyze_all_frames(label_statistics)
register_function(regionprops_table_all_frames, menu="Measurement > Label statistics of all frames (clEsperanto)")

def copy_keys(source, target, keys):
    for k in keys:
        target[k] = source[k]


@register_function(menu="Measurement > Statistics of labeled pixels (deprecated, clEsperanto)")
def statistics_of_labeled_pixels(image: "napari.types.ImageData", labels: "napari.types.LabelsData", measure_background=False, napari_viewer : "napari.Viewer"=None) -> "pandas.DataFrame":
    """
    Adds a table widget to a given napari viewer with quantitative analysis results derived from an image-labelimage pair.
    """
    warnings.warn("'Statistics of labeled pixels' is deprecated. Use 'Label statistics' instead.")

    if image is not None and labels is not None:

        # quantitative analysis using clEsperanto's statistics_of_labelled_pixels
        if measure_background:
            table = cle.statistics_of_background_and_labelled_pixels(image, labels)
        else:
            table = cle.statistics_of_labelled_pixels(image, labels)

        if napari_viewer is not None:
            # Store results in the properties dictionary:
            from napari_workflows._workflow import _get_layer_from_data
            labels_layer = _get_layer_from_data(napari_viewer, labels)
            labels_layer.properties = table

            # turn table into a widget
            from napari_skimage_regionprops import add_table
            add_table(labels_layer, napari_viewer)
        else:
            import pandas
            return pandas.DataFrame(table)
    else:
        warnings.warn("Image and labels must be set.")

