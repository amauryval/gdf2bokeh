import pytest


import geopandas as gpd

from shapely.geometry import Polygon


multipolygons = "tests/fixtures/multipolygons.geojson"
polygons = "tests/fixtures/polygons.geojson"
points = "tests/fixtures/points.geojson"
linestrings = "tests/fixtures/linestrings.geojson"
multilinestrings = "tests/fixtures/multilinestrings.geojson"
mixed_features = "tests/fixtures/mixed_features.geojson"


def open_geojson_to_gpd(input_file_path):
    return gpd.GeoDataFrame.from_file(input_file_path)


@pytest.fixture
def empty_data():
    empty_gdf = gpd.GeoDataFrame()
    empty_gdf['geometry'] = None
    return empty_gdf


@pytest.fixture
def mixed_features_data():
    return open_geojson_to_gpd(mixed_features)


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


@pytest.fixture
def polygon_from_coords_without_crs():
    lat_points = [50.9, 52.5, 50.0, 48.8, 50.9]
    lon_points = [4.4, 13.4, 14.4, 2.4, 4.4]
    polygon_geom = Polygon(zip(lon_points , lat_points))
    return gpd.GeoDataFrame(index=[0], geometry=[polygon_geom])


@pytest.fixture
def geom_wkt():
    return "LINESTRING(0 0, 25 25)"