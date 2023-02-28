from typing import Dict, List, Literal

import geopandas as gpd
import pandas as pd

from shapely import wkt

from gdf2bokeh.core import AppMap, ErrorGdf2Bokeh, GeomTypes, PointLayer, LinestringLayer, PolygonLayer, \
    LayerCore
from gdf2bokeh.helpers.geometry import get_gdf_geom_type
from gdf2bokeh.models import GeomFormat


class Gdf2Bokeh(AppMap):
    _layers = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear_layers()

    def clear_layers(self):
        """To remove all the layers"""
        self._layers = {}

    def add_layers_on_maps(self):
        for _, layer in self.layers.items():

            layer.render(self.figure)
            self._legend_settings()

    def add_layer_from_geodataframe(self, title: str, data: gpd.GeoDataFrame) -> None:
        """Add layer from a GeoDataframe"""
        if data.shape[0] == 0:
            raise ValueError("Geodataframe is empty")
        geom_types_on_data = get_gdf_geom_type(data, "geometry")
        geom_type = GeomTypes.has_value(geom_types_on_data)

        if geom_type == GeomTypes.POINT:
            layer = PointLayer(title=title, data=data)
        elif geom_type == GeomTypes.LINESTRINGS:
            layer = LinestringLayer(title=title, data=data)
        elif geom_type == GeomTypes.POLYGONS:
            layer = PolygonLayer(title=title, data=data)
        else:
            raise ValueError(f"{geom_type} not supported")
        self.layers = layer

    def add_layer_from_dataframe(self, title: str, data: pd.DataFrame, geom_column: str = "geometry",
                                 geom_format: str = "shapely") -> None:
        """Add layer from a Dataframe"""
        if geom_format == GeomFormat.SHAPELY:
            # all is good
            pass
        elif geom_format == GeomFormat.WKT:
            data[geom_column] = gpd.GeoSeries.from_wkt(data[geom_column])
        data = gpd.GeoDataFrame(data, geometry=geom_column)
        self.add_layer_from_geodataframe(title, data)

    def add_layer_from_list_dict(self, title: str, data: List[Dict], geom_column: str = "geometry",
                                 geom_format: str = "shapely") -> None:
        """Add layer from a list of dict"""
        data = pd.DataFrame(data)
        self.add_layer_from_dataframe(title, data, geom_column, geom_format)

    @property
    def layers(self) -> Dict[str, LayerCore] | None:
        """To return all or one layer"""
        return self._layers

    @layers.setter
    def layers(self, data: LayerCore) -> None:
        """To add a layer"""
        self._layers[data.title] = data
