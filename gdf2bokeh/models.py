from enum import Enum


class GeomFormat(str, Enum):
    SHAPELY = "shapely"
    WKT = "wkt"

    # TODO maybe useless
    def __str__(self) -> str:
        return str.__str__(self)
