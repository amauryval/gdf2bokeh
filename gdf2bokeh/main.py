from typing import Dict
from typing import List

import geopandas as gpd
import pandas as pd
import shapely.geometry.base

from gdf2bokeh.app_map import AppMap

from gdf2bokeh.layer import GeomTypes, MultiPointLayer
from gdf2bokeh.layer import PointLayer
from gdf2bokeh.layer import LinestringLayer
from gdf2bokeh.layer import PolygonLayer
from gdf2bokeh.layer import LayerCore

from gdf2bokeh.geometry import get_gdf_geom_type
from gdf2bokeh.models import GeomFormat


class Gdf2BokehError(Exception):
    pass


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

    def add_layer_from_geodataframe(self, title: str, data: gpd.GeoDataFrame, from_epsg: int,
                                    **style_parameters) -> None:
        """Add layer from a GeoDataframe"""
        if data.shape[0] == 0:
            raise Gdf2BokehError("GeoDataFrame is empty")

        if not self.is_df_empty(data):
            geom_types_on_data = get_gdf_geom_type(data, "geometry")
            geom_type = GeomTypes.has_value(geom_types_on_data)

            if geom_type == GeomTypes.POINT:
                self.layers = PointLayer(title=title, data=data, from_epsg=from_epsg, **style_parameters)
            elif geom_type == GeomTypes.LINESTRINGS:
                self.layers = LinestringLayer(title=title, data=data, from_epsg=from_epsg, **style_parameters)
            elif geom_type == GeomTypes.POLYGONS:
                self.layers = PolygonLayer(title=title, data=data, from_epsg=from_epsg, **style_parameters)
            elif geom_type == GeomTypes.MULTIPOINT:
                self.layers = MultiPointLayer(title=title, data=data, from_epsg=from_epsg, **style_parameters)
            else:
                raise ValueError(f"{geom_type} not supported")

    def add_layer_from_dataframe(self, title: str, data: pd.DataFrame, from_epsg: int, geom_column: str = "geometry",
                                 geom_format: str = "shapely", **style_parameters) -> None:
        """Add layer from a Dataframe"""
        if geom_format == GeomFormat.SHAPELY:
            # default behavior
            pass
        elif geom_format == GeomFormat.WKT:
            data[geom_column] = gpd.GeoSeries.from_wkt(data[geom_column])
        if not self.is_df_empty(data):
            data = gpd.GeoDataFrame(data, geometry=geom_column, crs=f"epsg:{from_epsg}")
            self.add_layer_from_geodataframe(title, data, from_epsg, **style_parameters)

    def add_layer_from_list_dict(self, title: str, data: List[Dict], from_epsg: int, geom_column: str = "geometry",
                                 geom_format: str = "shapely", **style_parameters) -> None:
        """Add layer from a list of dict"""
        data = pd.DataFrame(data)
        self.add_layer_from_dataframe(title, data, from_epsg, geom_column, geom_format, **style_parameters)

    def add_layer_from_dict_list(self, title: str, data: List[Dict], from_epsg: int, geom_column: str = "geometry",
                                 geom_format: str = "shapely", **style_parameters) -> None:
        """Add layer from a list of dict"""
        data = pd.DataFrame(data)
        self.add_layer_from_dataframe(title, data, from_epsg, geom_column, geom_format, **style_parameters)

    def add_layer_from_geom_list(self, title: str, data: List[str | shapely.geometry.base.BaseGeometry], from_epsg: int,
                                 geom_format: str = "shapely", **style_parameters) -> None:
        """Add layer from a geom (shapely, wkt) list"""
        data = [{"uuid": enum, "geometry": item} for enum, item in enumerate(data)]
        self.add_layer_from_dict_list(title, data, from_epsg, "geometry", geom_format, **style_parameters)

    @property
    def layers(self) -> Dict[str, LayerCore] | None:
        """To return all or one layer"""
        return self._layers

    @layers.setter
    def layers(self, data: LayerCore) -> None:
        """To add a layer"""
        self._layers[data.title] = data

    @staticmethod
    def is_df_empty(data: pd.DataFrame | gpd.GeoDataFrame) -> bool:
        if data.shape[0] == 0:
            return True
        return False
