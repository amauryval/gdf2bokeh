from typing import List, Set

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

import geopandas as gpd


def geometry_2_bokeh_format(geometry: base, coord_output_format: str = "xy") -> List[float | tuple[float]]:
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
            f"{geometry.geom_type} not supported"
        )

    return coord_values


def get_gdf_geom_type(input_gdf: gpd.GeoDataFrame, geom_col: str) -> Set[str]:
    return set(input_gdf[geom_col].geom_type.unique())
