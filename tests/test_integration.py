import pytest

import geopandas as gpd

from gdf2bokeh import Gdf2Bokeh
from gdf2bokeh.layer import GeomTypeError


def test_from_geodataframe(multipolygons_data):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geodataframe("layer_1", multipolygons_data, from_epsg=4326)

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 3
    assert layer.title == "layer_1"

    map_session.add_layers_on_maps()


def test_from_multipoints_geodataframe(multipoints_data):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geodataframe("layer_1", multipoints_data, from_epsg=4326)

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    # multipoint are exploded to be mapped
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"

    map_session.add_layers_on_maps()


def test_from_wkt_feature_list(data_wkt_list):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_dict_list("layer_1", data_wkt_list, from_epsg=4326, geom_format="wkt", size=6,
                                         fill_color="red", line_color="blue")

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"


def test_from_shapely_feature_list(data_shapely_list):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_dict_list("layer_1", data_shapely_list, from_epsg=4326)
    map_session.add_layer_from_dict_list("layer_2", [], from_epsg=4326)

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"

def test_from_shapely_feature_list_empty():
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_dict_list("layer_1", [], from_epsg=4326)

    layers = map_session.layers
    assert len(layers) == 0

    assert isinstance(layers, dict)


def test_from_wkt_geom_list(geom_wkt):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geom_list("layer_1", [geom_wkt, geom_wkt], from_epsg=4326, geom_format="wkt")

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"


def test_from_mutilinestring_geom(shapely_multilinestring_without_continuity):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geom_list("layer_1", [shapely_multilinestring_without_continuity], from_epsg=4326,
                                         geom_format="shapely")

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"


def test_from_dummy_shapely_geom_list(shapely_point, shapely_polygon):
    map_session = Gdf2Bokeh()
    with pytest.raises(GeomTypeError):
        map_session.add_layer_from_geom_list("layer_1", [shapely_point, shapely_polygon], from_epsg=4326,
                                             geom_format="shapely")
