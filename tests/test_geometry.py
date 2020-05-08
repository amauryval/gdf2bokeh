from bokeh_for_map.helpers.geometry import geometry_2_bokeh_format


def compute_geometry(data):
    x_values = data['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'x')).tolist()
    y_values = data['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'y')).tolist()
    return x_values, y_values


def test_points_geom_to_bokeh_format(points_data):
    x_values, y_values = compute_geometry(points_data)

    assert points_data.shape[0] == 3
    assert len(x_values) == 3
    assert len(y_values) == 3


def test_linestrings_geom_to_bokeh_format(linestrings_data):
    x_values, y_values = compute_geometry(linestrings_data)

    assert linestrings_data.shape[0] == 2
    assert len(x_values) == 2
    assert len(x_values[0]) == 2
    assert len(x_values[-1]) == 3
    assert len(y_values) == 2
    assert len(y_values[0]) == 2
    assert len(y_values[-1]) == 3


def test_multipolygons_geom_to_bokeh_format(multipolygons_data):
    x_values, y_values = compute_geometry(multipolygons_data)

    assert multipolygons_data.shape[0] == 2
    assert len(x_values) == 2
    assert len(x_values[0]) == 2
    assert len(x_values[0][0]) == 1
    assert len(x_values[0][-1]) == 3
    assert len(x_values[0][-1][0]) == 5
    assert len(x_values[0][-1][-1]) == 5
    assert len(x_values[-1]) == 1
    assert len(x_values[-1][0]) == 1
    assert len(x_values[-1][0][0]) == 5
    assert len(y_values) == 2
    assert len(y_values[0]) == 2
    assert len(y_values[0][0]) == 1
    assert len(y_values[0][-1]) == 3
    assert len(y_values[0][-1][0]) == 5
    assert len(y_values[0][-1][-1]) == 5
    assert len(y_values[-1]) == 1
    assert len(y_values[-1][0]) == 1
    assert len(y_values[-1][0][0]) == 5


def test_polygons_geom_to_bokeh_format(polygons_data):
    x_values, y_values = compute_geometry(polygons_data)

    assert polygons_data.shape[0] == 2
    assert len(x_values) == 2
    assert len(x_values[0]) == 2
    assert len(x_values[0][0]) == 1
    assert len(x_values[0][-1]) == 1
    assert len(y_values) == 2
    assert len(y_values[0]) == 2
    assert len(y_values[0][0]) == 1
    assert len(y_values[0][-1]) == 1


def test_multilines_geom_to_bokekeh_format(multilines_data):
    x_values, y_values = compute_geometry(multilines_data)

    assert multilines_data.shape[0] == 2
    assert len(x_values) == 2
    assert len(x_values[0]) == 4
    assert len(y_values) == 2
    assert len(y_values[0]) == 4
