
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

expected_node_style = [
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
    "x",
]

map_background_providers = {
    "CARTODBPOSITRON": get_provider(CARTODBPOSITRON),
    "CARTODBPOSITRON_RETINA": get_provider(CARTODBPOSITRON_RETINA),
    "ESRI_IMAGERY": get_provider(ESRI_IMAGERY),
    "OSM": get_provider(OSM),
    "STAMEN_TERRAIN": get_provider(STAMEN_TERRAIN),
    "STAMEN_TERRAIN_RETINA": get_provider(STAMEN_TERRAIN_RETINA),
    "STAMEN_TONER": get_provider(STAMEN_TONER),
    "STAMEN_TONER_BACKGROUND": get_provider(STAMEN_TONER_BACKGROUND),
    "STAMEN_TONER_LABELS": get_provider(STAMEN_TONER_LABELS)
}