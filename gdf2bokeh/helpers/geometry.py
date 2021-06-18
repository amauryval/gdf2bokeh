from typing import List
from typing import Union

from shapely.geometry import base
from shapely.geometry import Point
from shapely.geometry import MultiPoint

from shapely.geometry import LineString
from shapely.geometry import LinearRing
from shapely.geometry import MultiLineString

from shapely.geometry import Polygon
from shapely.geometry.polygon import InteriorRingSequence
from shapely.geometry import MultiPolygon

from shapely.geometry import GeometryCollection

import pandas as pd
import geopandas as gpd
from shapely.wkt import loads


def geometry_2_bokeh_format(geometry: base, coord_output_format: str = "xy") -> List:
    """
    geometry_2_bokeh_format

    To convert the geometry to display it with the bokeh library

    :type geometry: shapely.geometry.*
    :type coord_output_format: str, default: xy (x or y)

    :return: float or list of tuple
    """
    assert coord_output_format in ["xy", "x", "y"], f"coordinates output format {coord_output_format} not supported"

    coord_values: List = []

    if isinstance(geometry, Point):
        if coord_output_format != "xy":
            coord_values = getattr(geometry, coord_output_format)
        else:
            coord_values = next(iter(geometry.coords))

    elif isinstance(geometry, Polygon):

        exterior = [geometry_2_bokeh_format(geometry.exterior, coord_output_format)]

        interiors = geometry_2_bokeh_format(geometry.interiors, coord_output_format)
        coord_values = [exterior, interiors]
        if len(interiors) == 0:
            coord_values = [exterior]

    elif isinstance(geometry, (LinearRing, LineString)):
        coord_values = [
            geometry_2_bokeh_format(Point(feat), coord_output_format)
            for feat in geometry.coords
        ]

    if isinstance(geometry, (MultiPolygon, MultiLineString)):
        for feat in geometry.geoms:
            coord_values.extend(geometry_2_bokeh_format(feat, coord_output_format))

    if isinstance(geometry, InteriorRingSequence):
        coord_values.extend(
            [geometry_2_bokeh_format(feat, coord_output_format) for feat in geometry]
        )

    if isinstance(geometry, (MultiPoint, GeometryCollection)):
        raise ValueError(
            f"no interest to handle {geometry.geom_type}"
        )

    return coord_values


def wkt_to_gpd(geom_wkt: str, geom_epsg: int = 3857) -> gpd.GeoDataFrame:
    """
    wkt_to_gpd

    To convert a wkt into a geodataframe

    :type geom_wkt: str
    :type geom_epsg: int

    :return: float or list of tuple
    """
    df = pd.DataFrame([{
        "geometry": loads(geom_wkt),
    }])
    geometry = df["geometry"]
    properties = df.drop(columns=["geometry"])

    return gpd.GeoDataFrame(
        properties,
        geometry=geometry,
        crs=f"EPSG:{geom_epsg}"
    )


def check_multilinestring_continuity(input_geometry: Union[LineString, MultiLineString]) -> list:
    """
    check_if_multilinestring_is_not_continuous

    If multilinestring continuity is not valid, we convert all of its elements to linestring, in order to display them
    correctly on bokeh

    :type input_geometry: shapely.geometry.lineString or shapely.geometry.MultiLineString

    :return: list of shapely.geometry.lineString/shapely.geometry.MultiLineString
    """
    if isinstance(input_geometry, MultiLineString):
        dict_line = {key: value for key, value in enumerate(input_geometry.geoms)}
        for key, line in dict_line.items():
            if key != 0 and dict_line[key - 1].coords[-1] == line.coords[-1]:
                # let's go to reorient
                dict_line[key] = LineString(line.coords[::-1])
            elif key != 0 and dict_line[key - 1].coords[-1] not in (line.coords[-1], line.coords[0]):
                # if line is not continuous
                return list(input_geometry.geoms)

        return [MultiLineString([geom for geom in dict_line.values()])]

    return [input_geometry]