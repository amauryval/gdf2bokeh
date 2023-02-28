from typing import List
from typing import Dict
from typing import Set

from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.tile_providers import CARTODBPOSITRON_RETINA
from bokeh.tile_providers import ESRI_IMAGERY
from bokeh.tile_providers import OSM
from bokeh.tile_providers import STAMEN_TERRAIN
from bokeh.tile_providers import STAMEN_TERRAIN_RETINA
from bokeh.tile_providers import STAMEN_TONER
from bokeh.tile_providers import STAMEN_TONER_BACKGROUND
from bokeh.tile_providers import STAMEN_TONER_LABELS
from bokeh.tile_providers import get_provider

expected_node_style: List[str] = [
    "asterisk",
    "circle",
    "circle_cross",
    "circle_x",
    "cross",
    "dash",
    "diamond",
    "diamond_cross",
    "hex",
    "inverted_triangle",
    "square",
    "square_cross",
    "square_x",
    "triangle",
    "star",
    "star_dot",
    "x",
    "y",
]  # https://docs.bokeh.org/en/latest/docs/reference/models/markers.html

map_background_providers: Dict = {
    "CARTODBPOSITRON": get_provider(CARTODBPOSITRON),
    "CARTODBPOSITRON_RETINA": get_provider(CARTODBPOSITRON_RETINA),
    "ESRI_IMAGERY": get_provider(ESRI_IMAGERY),
    "OSM": get_provider(OSM),
    "STAMEN_TERRAIN": get_provider(STAMEN_TERRAIN),
    "STAMEN_TERRAIN_RETINA": get_provider(STAMEN_TERRAIN_RETINA),
    "STAMEN_TONER": get_provider(STAMEN_TONER),
    "STAMEN_TONER_BACKGROUND": get_provider(STAMEN_TONER_BACKGROUND),
    "STAMEN_TONER_LABELS": get_provider(STAMEN_TONER_LABELS),
}

linestrings_type_compatibility: Set[str] = {"LineString", "MultiLineString"}
polygons_type_compatibility: Set[str] = {"Polygon", "MultiPolygon"}
point_type_compatibility: Set[str] = {"Point"}
geometry_compatibility: List[Set[str]] = [
    linestrings_type_compatibility,
    polygons_type_compatibility,
    point_type_compatibility,
]
