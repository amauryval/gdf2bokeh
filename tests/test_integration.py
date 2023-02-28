import pytest

import geopandas as gpd
from bokeh.models import ColumnDataSource

from gdf2bokeh import Gdf2Bokeh
from gdf2bokeh.layer import GeomTypeError


def test_from_geodataframe(multipolygons_data):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geodataframe("layer_1", multipolygons_data)

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 3
    assert layer.title == "layer_1"
    assert isinstance(layer.bokeh_data, ColumnDataSource)
    assert isinstance(layer.bokeh_data_structure, ColumnDataSource)

    map_session.add_layers_on_maps()


def test_from_wkt_feature_list(data_wkt_list):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_dict_list("layer_1", data_wkt_list, geom_format="wkt")

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"


def test_from_shapely_feature_list(data_shapely_list):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_dict_list("layer_1", data_shapely_list)

    layers = map_session.layers
    assert len(layers) == 1

    layer = layers["layer_1"]
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.shape[0] == 2
    assert layer.data.shape[-1] == 2
    assert layer.title == "layer_1"


def test_from_wkt_geom_list(geom_wkt):
    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geom_list("layer_1", [geom_wkt, geom_wkt], geom_format="wkt")

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
        map_session.add_layer_from_geom_list("layer_1", [shapely_point, shapely_polygon], geom_format="shapely")
