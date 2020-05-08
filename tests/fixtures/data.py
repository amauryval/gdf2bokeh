import pytest


import geopandas as gpd




multipolygons = "fixtures/multipolygons.geojson"
polygons = "fixtures/polygons.geojson"
points = "fixtures/points.geojson"
linestrings = "fixtures/linestrings.geojson"
multilinestrings = "fixtures/multilinestrings.geojson"


def open_geojson_to_gpd(input_file_path):
    return gpd.GeoDataFrame.from_file(input_file_path)


@pytest.fixture
def multipolygons_data():
    return open_geojson_to_gpd(multipolygons)


@pytest.fixture
def polygons_data():
    return open_geojson_to_gpd(polygons)


@pytest.fixture
def linestrings_data():
    return open_geojson_to_gpd(linestrings)


@pytest.fixture
def multilines_data():
    return open_geojson_to_gpd(multilinestrings)


@pytest.fixture
def points_data():
    return open_geojson_to_gpd(points)