from gdf2bokeh.helpers.geometry import geometry_2_bokeh_format
from gdf2bokeh.helpers.geometry import wkt_to_gpd

import itertools


def compute_geometry(data):
    x_values = data['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'x')).tolist()
    y_values = data['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'y')).tolist()
    return x_values, y_values


def test_points_geom_to_bokeh_format(points_data):
    x_values, y_values = compute_geometry(points_data)

    assert len(x_values) == points_data.shape[0]
    assert x_values == list(map(lambda feature: feature.x, points_data.geometry.to_list()))

    assert len(y_values) == points_data.shape[0]
    assert y_values == list(map(lambda feature: feature.y, points_data.geometry.to_list()))


def test_linestrings_geom_to_bokeh_format(linestrings_data):
    x_values, y_values = compute_geometry(linestrings_data)

    assert len(x_values) == linestrings_data.shape[0]
    # first object
    assert x_values[0] == list(linestrings_data.iloc[0].geometry.xy[0])
    # sec object
    assert x_values[-1] == list(linestrings_data.iloc[-1].geometry.xy[0])

    assert len(y_values) == linestrings_data.shape[0]
    # first object
    assert y_values[0] == list(linestrings_data.iloc[0].geometry.xy[-1])
    # sec object
    assert y_values[-1] == list(linestrings_data.iloc[-1].geometry.xy[-1])


def test_multipolygons_geom_to_bokeh_format(multipolygons_data):
    x_values, y_values = compute_geometry(multipolygons_data)

    assert len(x_values) == multipolygons_data.shape[0]
    assert len(x_values[0]) == 1
    assert len(x_values[0][0]) == 1
    # first object
    assert len(x_values[0][-1]) == 1
    assert x_values[0][-1][0] == list(multipolygons_data.iloc[0].geometry.exterior.xy[0])
    # sec object
    assert len(x_values[-1][0]) == 1
    exteriors = [[list(geom.exterior.xy[0])] for geom in multipolygons_data.iloc[-1].geometry.geoms]
    interiors = [
        list(map(lambda feat: list(feat.xy[0]), geom.interiors))
        for geom in filter(lambda x: len(x.interiors) > 0, multipolygons_data.iloc[-1].geometry.geoms)
    ]
    assert sorted(exteriors + interiors) == sorted(x_values[-1])
    assert len(y_values) == multipolygons_data.shape[0]
    assert len(y_values[0]) == 1
    assert len(y_values[0][0]) == 1
    assert len(y_values[0][-1]) == 1
    # first object
    assert y_values[0][-1][0] == list(multipolygons_data.iloc[0].geometry.exterior.xy[-1])
    assert len(y_values[-1][0]) == 1
    # sec object
    exteriors = [[list(geom.exterior.xy[-1])] for geom in multipolygons_data.iloc[-1].geometry.geoms]
    interiors = [
        list(map(lambda feat: list(feat.xy[-1]), geom.interiors))
        for geom in filter(lambda x: len(x.interiors) > 0, multipolygons_data.iloc[-1].geometry.geoms)
    ]
    assert sorted(exteriors + interiors) == sorted(y_values[-1])


def test_polygons_geom_to_bokeh_format(polygons_data):
    x_values, y_values = compute_geometry(polygons_data)

    assert len(x_values) == polygons_data.shape[0]
    assert len(y_values) == polygons_data.shape[0]
    assert len(x_values[0]) == 2  # 2 meaning exterior(1) AND interiors(1)
    assert len(y_values[0]) == 2  # 2 meaning exterior(1) AND interiors(1)
    assert len(x_values[-1]) == 1  # 1 meaning exterior(1) AND interiors(0)
    assert len(y_values[-1]) == 1  # 1 meaning exterior(1) AND interiors(0)

    # first object
    assert len(x_values[0][0]) == 1
    assert x_values[0][0][0] == list(polygons_data.iloc[0].geometry.exterior.xy[0])
    exterior_count = 1  # because it a polygon
    assert x_values[0][0][0] == list(polygons_data.iloc[0].geometry.exterior.xy[0])
    # holes
    assert x_values[0][exterior_count - len(x_values[0])] == list(list(interior.xy[0]) for interior in polygons_data.iloc[0].geometry.interiors)
    # sec object
    assert x_values[-1][0][0] == list(polygons_data.iloc[-1].geometry.exterior.xy[0])
    assert x_values[-1][0][-1] == list(polygons_data.iloc[-1].geometry.exterior.xy[0])

    assert len(y_values[0][0]) == 1
    # first object
    assert y_values[0][0][0] == list(polygons_data.iloc[0].geometry.exterior.xy[-1])
    assert y_values[0][0][-1] == list(polygons_data.iloc[0].geometry.exterior.xy[-1])
    exterior_count = 1  # because it a polygon
    assert y_values[0][0][0] == list(polygons_data.iloc[0].geometry.exterior.xy[-1])
    # holes
    assert y_values[0][exterior_count - len(y_values[0])] == list(list(interior.xy[-1]) for interior in polygons_data.iloc[0].geometry.interiors)
    # sec object
    assert y_values[-1][0][0] == list(polygons_data.iloc[-1].geometry.exterior.xy[-1])
    assert y_values[-1][0][-1] == list(polygons_data.iloc[-1].geometry.exterior.xy[-1])


def test_multilines_geom_to_bokekeh_format(multilines_data):
    x_values, y_values = compute_geometry(multilines_data)

    assert len(x_values) == multilines_data.shape[0]
    assert len(y_values) == multilines_data.shape[0]

    # first object
    assert x_values[0] == list(multilines_data.iloc[0].geometry.xy[0])
    # sec object
    assert x_values[-1] == list(itertools.chain.from_iterable(
        [list(geom.xy[0]) for geom in multilines_data.iloc[-1].geometry.geoms]
    ))

    assert y_values[0] == list(multilines_data.iloc[0].geometry.xy[-1])
    assert y_values[-1] == list(itertools.chain.from_iterable(
        [list(geom.xy[-1]) for geom in multilines_data.iloc[-1].geometry.geoms]
    ))


def test_wkt_to_gpd(geom_wkt):
    output_gdf = wkt_to_gpd(geom_wkt)
    assert output_gdf.shape[0] == 1
    assert output_gdf.shape[-1] == 2
