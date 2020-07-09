import geopandas as gpd

from geo_bokeh import BokehForMap


def test_bokeh_session(width, height):
    my_map = BokehForMap("My beautiful map", width, height)

    assert my_map.figure.plot_height == height
    assert my_map.figure.plot_width == width


def test_bokeh_processing(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):
    my_map = BokehForMap("My beautiful map")

    bokeh_multipolygons = my_map.format_gdf_features_to_bokeh(multipolygons_data)
    my_map.add_polygons(
        bokeh_multipolygons,
        fill_color="orange",
        legend="MultiPolygons"
    )

    bokeh_polygons = my_map.format_gdf_features_to_bokeh(polygons_data)
    my_map.add_polygons(
        bokeh_polygons,
        fill_color="orange",
        legend="Polygons"
    )

    bokeh_linestrings = my_map.format_gdf_features_to_bokeh(linestrings_data)
    my_map.add_lines(
        bokeh_linestrings,
        color="orange",
        legend="linestrings"
    )

    bokeh_multilines = my_map.format_gdf_features_to_bokeh(multilines_data)
    my_map.add_lines(
        bokeh_multilines,
        color="orange",
        legend="multilinestrings"
    )

    bokeh_points = my_map.format_gdf_features_to_bokeh(points_data)
    my_map.add_points(
        bokeh_points,
        fill_color="orange",
        legend="points",
        style="diamond"
    )

    assert len(my_map.figure.renderers) == 6
    assert len(my_map.figure.tools) == 10
    # TODO improve !


def test_bokeh_structure(multipolygons_data):
    my_map = BokehForMap("My beautiful map")

    points_input = my_map.get_bokeh_structure_from_gdf_features(multipolygons_data)

    assert set(points_input.data.keys()) == {"x", "y", "name", "value"}
    assert len(points_input.data.values()) == 4
    for value in points_input.data.values():
        assert isinstance(value, list)
