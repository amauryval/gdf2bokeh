from typing import Dict, List, Literal

import geopandas as gpd
import pandas as pd

from shapely import wkt

from gdf2bokeh.core import AppMap, ErrorGdf2Bokeh
from gdf2bokeh.helpers.geometry import get_gdf_geom_type
from gdf2bokeh.models import GeomFormat, Layer, BokehGeomTypes


class Gdf2Bokeh(AppMap):
    _layers = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear_layers()

    def clear_layers(self):
        """To remove all the layers"""
        self._layers = {}

    def add_layers_on_maps(self):
        for title, layer in self.layers.items():
            if layer.geom_type == BokehGeomTypes.POINT:
                bokeh_container = self.add_points(layer)
            if layer.geom_type == BokehGeomTypes.LINESTRINGS:
                bokeh_container = self.add_lines(layer)
            if layer.geom_type == BokehGeomTypes.POLYGONS:
                bokeh_container = self.add_polygons(layer)
            else:
                raise ErrorGdf2Bokeh("It should not happened")

    def add_layer_from_geodataframe(self, title: str, data: gpd.GeoDataFrame) -> None:
        """Add layer from a GeoDataframe"""
        if data.shape[0] == 0:
            raise ValueError("Geodataframe is empty")
        geom_types_on_data = get_gdf_geom_type(data, "geometry")
        geom_type = BokehGeomTypes.has_value(geom_types_on_data)
        # data = self._format_gdf_features_to_bokeh(data)
        self.layers = Layer(title=title, data=data, geom_type=geom_type)


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
    def layers(self, title: str | None = None) -> Dict[str, Layer] | None:
        """To return all or one layer"""
        if title is not None:
            return self._layers.get(title, None)
        return self._layers

    @layers.setter
    def layers(self, data: Layer) -> None:
        """To add a layer"""
        self._layers[data.title] = data
