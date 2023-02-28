from dataclasses import dataclass
from enum import Enum
from typing import List
from typing import Optional
from typing import Dict
from typing import Set
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Any

import geopandas as gpd
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.renderers import GlyphRenderer

from bokeh.models import HoverTool
from bokeh.palettes import brewer

from gdf2bokeh.helpers.geometry import geometry_2_bokeh_format
from gdf2bokeh.helpers.geometry import check_multilinestring_continuity

from gdf2bokeh.helpers.settings import expected_node_style
from gdf2bokeh.helpers.settings import map_background_providers


class GeomTypes(set, Enum):
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
        for enum in GeomTypes.__members__.values():
            if item.issubset(enum):
                return enum
        raise ValueError(f"{item} not supported")


class Layer:

    title = None
    _data = None
    geom_type = None

    __GEOMETRY_FIELD_NAME: str = "geometry"
    _DEFAULT_EPSG: int = 3857

    def __init__(self, title: str, data: gpd.GeoDataFrame, geom_type: 'GeomTypes'):
        super().__init__()

        self.title = title
        self._data = data
        self.geom_type = geom_type

    @property
    def data(self) -> gpd.GeoDataFrame:
        return self._data

    @data.setter
    def data(self, data: gpd.GeoDataFrame) -> None:
        expected_epsg = f"epsg:{self._DEFAULT_EPSG}"
        if data.crs != expected_epsg:
            data = self._data.to_crs(expected_epsg)
        self._data = data

    def bokeh_data(self):
        if self.geom_type in [GeomTypes.POINT, GeomTypes.POLYGONS]:
            return self._format_gdf_features_to_bokeh(self.data)

        if self.geom_type == GeomTypes.LINESTRINGS:
            # go to check the multilinestring continuity, because the bokeh format cannot display a multilinestring
            # containing a discontinuity. We'll convert the objet into linestring if needed.
            data = self.__post_proc_multilinestring_gdf(self.data)
            return self._format_gdf_features_to_bokeh(data)

        else:
            raise ErrorGdf2Bokeh("It should not happened")

    def bokeh_data_structure(self) -> ColumnDataSource:
        """
        To build the bokeh data structure from a GeoDataframe.
        """
        data = self.data.head(1)
        data = self._format_gdf_features_to_bokeh(data)
        return ColumnDataSource(data=dict.fromkeys(data.column_names, []))

    @staticmethod
    def __post_proc_multilinestring_gdf(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        input_gdf_proceed = input_gdf.copy(deep=True)
        input_gdf_proceed["geometry"] = input_gdf_proceed["geometry"].apply(
            lambda x: check_multilinestring_continuity(x)
        )
        input_gdf_proceed = input_gdf_proceed.explode("geometry")
        return input_gdf_proceed

    @staticmethod
    def _format_gdf_features_to_bokeh(data: gpd.GeoDataFrame) -> ColumnDataSource:

        bokeh_data = ColumnDataSource(
            {
                **{
                    "x": data["geometry"]
                    .apply(lambda x: geometry_2_bokeh_format(x, "x"))
                    .tolist(),
                    "y": data["geometry"]
                    .apply(lambda x: geometry_2_bokeh_format(x, "y"))
                    .tolist(),
                },
                **{
                    column: data[column].to_list()
                    for column in data.columns
                    if column != "geometry"
                },
            }
        )
        return bokeh_data


class ErrorGdf2Bokeh(Exception):
    pass


class AppMap:

    def __init__(
        self,
        title: str = "My empty Map",
        width: int = 800,
        height: int = 600,
        background_map_name: str = "CARTODBPOSITRON",
    ) -> None:
        """
        :param title: figure title
        :type title: str
        :param width: width value
        :type width: int
        :param height: height value
        :type height: int
        :param background_map_name: background map name
        :type background_map_name: str
        """
        super().__init__()

        self.__BOKEH_LAYER_CONTAINERS: Dict = {}

        self.figure = figure(
            title=title,
            output_backend="webgl",
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )

        self.figure.width = width
        self.figure.height = height

        self._add_background_map(background_map_name)

    def _legend_settings(self) -> None:
        # interactive legend
        self.figure.legend.click_policy = "hide"

    def _add_background_map(self, background_map_name: str) -> None:
        assert (
            background_map_name in map_background_providers.keys()
        ), f"Use one of these background map : {', '.join(map_background_providers)}"
        self.figure.add_tile(map_background_providers[background_map_name])

    def _set_tooltip_from_features(
        self, features: ColumnDataSource, rendered: GlyphRenderer
    ) -> None:

        column_tooltip = self.__build_column_tooltip(features)
        self.figure.add_tools(
            HoverTool(tooltips=column_tooltip, renderers=[rendered], mode="mouse")
        )
    
    @staticmethod
    def __build_column_tooltip(features_column_data_source: ColumnDataSource) -> List[Tuple[str, str]]:
        columns = list(filter(lambda x: x not in ["x", "y"], features_column_data_source.data.keys()))
        return list(
            zip(map(lambda x: str(x.upper()), columns), map(lambda x: f"@{x}", columns))
        )
    

