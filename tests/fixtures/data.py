import pytest


import geopandas as gpd




multipolygons = "tests/fixtures/multipolygons.geojson"
polygons = "tests/fixtures/polygons.geojson"
points = "tests/fixtures/points.geojson"
linestrings = "tests/fixtures/linestrings.geojson"
multilinestrings = "tests/fixtures/multilinestrings.geojson"


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

@pytest.fixture
def width():
    return 640

@pytest.fixture
def height():
    return 480