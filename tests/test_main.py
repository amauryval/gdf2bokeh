import pytest


from easy_map_bokeh import EasyMapBokeh


def test_bokeh_session(width, height):
    my_map = EasyMapBokeh("My beautiful map" , width , height)

    assert my_map.figure.plot_height == height
    assert my_map.figure.plot_width == width


def test_bokeh_processing(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):
    my_map = EasyMapBokeh("My beautiful map")

    my_map.add_polygons(
        multipolygons_data,
        fill_color="orange",
        legend="MultiPolygons"
    )

    my_map.add_polygons(
        polygons_data,
        fill_color="orange",
        legend="Polygons"
    )

    my_map.add_lines(
        linestrings_data,
        color="orange",
        legend="linestrings"
    )

    my_map.add_lines(
        multilines_data,
        color="orange",
        legend="multilinestrings"
    )

    my_map.add_points(
        points_data,
        fill_color="orange",
        legend="points",
        style="diamond"
    )

    assert len(my_map.figure.renderers) == 6
    assert len(my_map.figure.tools) == 10
    assert len(my_map.get_bokeh_layer_containers) == 5


def test_bokeh_processing_with_gdf_without_crs(polygon_from_coords_without_crs):
    my_map = EasyMapBokeh("My beautiful map")
    with pytest.raises(ValueError) as excinfo:
        my_map.add_polygons(
            polygon_from_coords_without_crs,
            fill_color="purple",
            legend="Tricky Polygons"
        )
    assert 'Cannot transform naive geometries.  Please set a crs on the object first.' in str(excinfo.value)


def test_bokeh_processing_with_layers_with_max_settings(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):

    layers_to_add = [
        {
            "input_gdf": multipolygons_data,
            "fill_color": "orange",
            "legend": "MultiPolygons"
        },
        {
            "input_gdf": polygons_data,
            "fill_color": "red",
            "legend": "Polygons"
        },
        {
            "input_gdf": linestrings_data,
            "color": "grey",
            "legend": "linestrings"
        },
        {
            "input_gdf": multilines_data,
            "color": "black",
            "legend": "multilinestrings"
        },
        {
            "input_gdf": points_data,
            "fill_color": "blue",
            "legend": "points",
            "style": "diamond"
        },
    ]
    my_map = EasyMapBokeh("My beautiful map", layers=layers_to_add)

    assert len(my_map.figure.renderers) == 8
    assert len(my_map.figure.tools) == 12
    assert len(my_map.get_bokeh_layer_containers) == 7


def test_bokeh_processing_with_layers_with_min_setting(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):

    layers_to_add = [
        {
            "input_gdf": multipolygons_data,
            "legend": "MultiPolygons"
        },
        {
            "input_gdf": polygons_data,
            "legend": "Polygons"
        },
        {
            "input_gdf": linestrings_data,
            "legend": "linestrings"
        },
        {
            "input_gdf": multilines_data,
            "color": "black",
            "legend": "multilinestrings"
        },
        {
            "input_gdf": points_data,
            "legend": "points",
        },
    ]
    my_map = EasyMapBokeh("My beautiful map", layers=layers_to_add)

    assert len(my_map.figure.renderers) == 8
    assert len(my_map.figure.tools) == 12
    assert len(my_map.get_bokeh_layer_containers) == 7

def test_bokeh_structure(multipolygons_data):

    points_input = EasyMapBokeh("hello").get_bokeh_structure_from_gdf(multipolygons_data)
    assert set(points_input.data.keys()) == {"x", "y", "geom_type", "name"}
    assert len(points_input.data.values()) == 4
    for value in points_input.data.values():
        assert isinstance(value, list)
