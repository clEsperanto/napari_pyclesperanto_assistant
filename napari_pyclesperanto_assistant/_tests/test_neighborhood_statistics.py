def test_neighborhood_statistics():
    import numpy as np
    labels = np.asarray([
        [0, 1],
        [2, 2],
        [3, 0]
    ])

    measurements = {
        "label":[1,2,3],
        "area":[1,2,1]
    }

    from napari_pyclesperanto_assistant._neighborhood_statistics import neighborhood_statistics_of_data

    result = neighborhood_statistics_of_data(labels, measurements,
                                             touching_neighbors=True,
                                             neighbors_of_touching_neighbors=True,
                                             proximal_neighbors=True,
                                             proximal_distance=1.5,
                                             n_nearest_neighbors=True,
                                             n=1,
                                             measure_mean_of_neighbors=True,
                                             measure_standard_deviation_of_neighbors=True,
                                             measure_minimum_of_neighbors=True,
                                             measure_maximum_of_neighbors=True,
                                             measure_median_of_neighbors=True,
                                             )
    print(result)

    assert len(result.keys()) == 22
    for k, v in result.items():
        assert len(v) == 3
