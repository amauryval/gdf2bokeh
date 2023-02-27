from collections.abc import Set
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

import geopandas as gpd


class BokehGeomTypes(set, Enum):
    LINESTRINGS = {"LineString", "MultiLineString"}
    POLYGONS = {"Polygon", "MultiPolygon"}
    POINT = {"Point"}
    # geometry_collection_type = [
    #     linestrings_types,
    #     polygons_types,
    #     point_types,
    # ]

    @staticmethod
    def has_value(item: set):
        for enum in BokehGeomTypes.__members__.values():
            if item.issubset(enum):
                return enum
        raise ValueError(f"{item} not supported")


@dataclass
class Layer:
    title: str
    data: gpd.GeoDataFrame
    geom_type: BokehGeomTypes


class GeomFormat(str, Enum):
    SHAPELY = "shapely"
    WKT = "wkt"

    def __str__(self) -> str:
        return str.__str__(self)
