from collections.abc import Set
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

import geopandas as gpd





class GeomFormat(str, Enum):
    SHAPELY = "shapely"
    WKT = "wkt"

    def __str__(self) -> str:
        return str.__str__(self)
