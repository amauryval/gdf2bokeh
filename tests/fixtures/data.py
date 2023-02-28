from typing import List, Dict

import pytest

import geopandas as gpd

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint


multipolygons = "tests/fixtures/multipolygons.geojson"
polygons = "tests/fixtures/polygons.geojson"
points = "tests/fixtures/points.geojson"
linestrings = "tests/fixtures/linestrings.geojson"
multilinestrings = "tests/fixtures/multilinestrings.geojson"
mixed_features = "tests/fixtures/mixed_features.geojson"


def open_geojson_to_gpd(input_file_path) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame.from_file(input_file_path)


@pytest.fixture
def empty_data() -> gpd.GeoDataFrame:
    empty_gdf = gpd.GeoDataFrame()
    empty_gdf['geometry'] = None
    return empty_gdf


@pytest.fixture
def data_shapely_list() -> List[Dict]:
    return [
        {
            "value": "coucou",
            "geometry": Point(0, 0)
        },
        {
            "value": "hello",
            "geometry": Point(1, 2)
        }
    ]


@pytest.fixture
def data_wkt_list() -> List[Dict]:
    return [
        {
            "value": "coucou",
            "geometry": 'POINT(0 0)'
        },
        {
            "value": "hello",
            "geometry": 'POINT(1 2)'
        }
    ]


@pytest.fixture
def mixed_features_data() -> gpd.GeoDataFrame:
    return open_geojson_to_gpd(mixed_features)


@pytest.fixture
def multipolygons_data() -> gpd.GeoDataFrame:
    return open_geojson_to_gpd(multipolygons)


@pytest.fixture
def polygons_data() -> gpd.GeoDataFrame:
    return open_geojson_to_gpd(polygons)


@pytest.fixture
def linestrings_data() -> gpd.GeoDataFrame:
    return open_geojson_to_gpd(linestrings)


@pytest.fixture
def multilines_data() -> gpd.GeoDataFrame:
    return open_geojson_to_gpd(multilinestrings)


@pytest.fixture
def points_data() -> gpd.GeoDataFrame:
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
    polygon_geom = Polygon(zip(lon_points, lat_points))
    return gpd.GeoDataFrame(index=[0], geometry=[polygon_geom])


@pytest.fixture
def geom_wkt():
    return "LINESTRING(0 0, 25 25)"


@pytest.fixture
def shapely_point():
    return Point(0.0, 1.0)


@pytest.fixture
def shapely_linestring():
    return LineString([(0, 0), (1, 2)])


@pytest.fixture
def shapely_polygon():
    return Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])


@pytest.fixture
def shapely_polygon_with_hole():
    return Polygon(
        ((0, 0), (10, 0), (10, 10), (0, 10), (0, 0)),
        (
            ((1, 2), (5, 2), (5, 1), (1, 1)),
            ((9, 9), (9, 8), (8, 8), (8, 9))
        )
    )


@pytest.fixture
def shapely_multilinestring_without_continuity():
    return MultiLineString([((0, 0), (5, 2)), ((6, 0), (10, 10))])


@pytest.fixture
def shapely_multilinestring_continuity():
    return MultiLineString([((0, 0), (5, 2)), ((5, 2), (10, 10))])


@pytest.fixture
def shapely_multilinestring_unordered():
    return MultiLineString([((0, 0), (5, 2)), ((10, 10), (5, 2))])


@pytest.fixture
def shapely_multipoint():
    return MultiPoint([(0, 0), (1, 1), (1, 2), (2, 2)])
