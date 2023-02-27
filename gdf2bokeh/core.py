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

if TYPE_CHECKING:
    from gdf2bokeh import Layer, BokehGeomTypes

from gdf2bokeh.helpers.geometry import geometry_2_bokeh_format
from gdf2bokeh.helpers.geometry import check_multilinestring_continuity

from gdf2bokeh.helpers.settings import expected_node_style
from gdf2bokeh.helpers.settings import map_background_providers

from gdf2bokeh.helpers.settings import default_attributes
from gdf2bokeh.helpers.settings import input_data_default_attributes

from gdf2bokeh.helpers.settings import geometry_compatibility
from gdf2bokeh.helpers.settings import linestrings_type_compatibility
from gdf2bokeh.helpers.settings import polygons_type_compatibility
from gdf2bokeh.helpers.settings import point_type_compatibility


class ErrorGdf2Bokeh(Exception):
    pass


class AppMap:

    __GEOMETRY_FIELD_NAME: str = "geometry"
    __DEFAULT_EPSG: int = 3857
    __BREWER_COLORS: List = brewer["Set3"][7]

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

        # self._layers_configuration = layers
        # if layers is not None:
        #     self.__add_layers()

    @property
    def get_bokeh_layer_containers(self) -> Dict:
        """
        To get all the bokeh layer containers in order to create dynamic layer (with slider for example)

        :return: bokeh layer container
        :rtype: dict
        """
        return self.__BOKEH_LAYER_CONTAINERS

    def get_bokeh_structure_from_gdf(
        self, features: gpd.GeoDataFrame
    ) -> ColumnDataSource:
        """
        To build the bokeh data structure from a GeoDataframe.

        :param features: your input GeoDataframe
        :type features: geopandas.GeoDataFrame
        :return: the bokeh data structure
        :rtype: bokeh.models.ColumnDataSource
        """
        assert isinstance(features, gpd.GeoDataFrame), "use a GeoDataframe please"

        bokeh_data = self.__convert_gdf_to_bokeh_data(features, get_gdf_structure=True)
        return ColumnDataSource(data=dict.fromkeys(bokeh_data.column_names, []))

    def __legend_settings(self) -> None:
        # interactive legend
        self.figure.legend.click_policy = "hide"

    def __reprojection(self, input_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        expected_epsg = f"epsg:{self.__DEFAULT_EPSG}"
        if input_data.crs != expected_epsg:

            return input_data.to_crs(expected_epsg)

        return input_data

    def add_lines(self, layer: "Layer", **kwargs) -> ColumnDataSource:
        """
        To add a lines layer on bokeh Figure (LineString and MultiLineString geometry types supported)

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        input_data = self.__post_proc_input_gdf(input_gdf)
        # go to check the multilinestring continuity, because the bokeh format cannot display a multilinestring
        # containing a discontinuity. We'll convert the objet into linestring if needed.
        input_data = self.__post_proc_multilinestring_gdf(input_data)
        bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)

        rendered = self.figure.multi_line(
            xs="x", ys="y", source=bokeh_layer_container, legend_label=layer.title, **kwargs
        )
        self._set_tooltip_from_features(bokeh_layer_container, rendered)
        self.__legend_settings()

        self.__BOKEH_LAYER_CONTAINERS[layer.title] = bokeh_layer_container
        return bokeh_layer_container

    def __post_proc_input_gdf(self, input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        input_gdf_proceed = input_gdf.copy(deep=True)
        input_gdf_proceed = self.__reprojection(input_gdf_proceed)

        return input_gdf_proceed

    @staticmethod
    def __post_proc_multilinestring_gdf(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        input_gdf_proceed = input_gdf.copy(deep=True)
        input_gdf_proceed["geometry"] = input_gdf_proceed["geometry"].apply(
            lambda x: check_multilinestring_continuity(x)
        )
        input_gdf_proceed = input_gdf_proceed.explode("geometry")
        return input_gdf_proceed

    def add_points(self, layer: "Layer", style: str = "circle", **kwargs) -> ColumnDataSource:
        """
        To add a points layer on bokeh Figure  (Point geometry type supported)

        :param style: node style, check expected_node_style variable
        :type style: str
        :param kwargs: arguments from bokeh to style the layer
        :type kwargs: str

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        assert (
            style in expected_node_style
        ), f"{style} not supported. Choose one of them : {', '.join(expected_node_style)}"

        input_data = self.__post_proc_input_gdf(layer.data)
        bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)

        rendered = getattr(self.figure, style)(
            x="x", y="y", source=bokeh_layer_container, legend_label=layer.title, **kwargs
        )
        self._set_tooltip_from_features(bokeh_layer_container, rendered)
        self.__legend_settings()

        self.__BOKEH_LAYER_CONTAINERS[layer.title] = bokeh_layer_container

        return bokeh_layer_container

    def add_polygons(self, layer: "Layer", **kwargs) -> ColumnDataSource:
        """
        To add a polygons layer on bokeh Figure (Polygon and MultiPolygon geometry type supported)

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        input_data = self.__post_proc_input_gdf(layer.data)
        bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)

        rendered = self.figure.multi_polygons(
            xs="x", ys="y", source=bokeh_layer_container, legend_label=layer.title,  **kwargs
        )
        self._set_tooltip_from_features(bokeh_layer_container, rendered)
        self.__legend_settings()

        self.__BOKEH_LAYER_CONTAINERS[layer.title] = bokeh_layer_container
        return bokeh_layer_container



    def _add_background_map(self, background_map_name: str) -> None:
        assert (
            background_map_name in map_background_providers.keys()
        ), f"Use one of these background map : {', '.join(map_background_providers)}"
        self.figure.add_tile(map_background_providers[background_map_name])

    def __get_geom_types_from_gdf(self, input_gdf: gpd.GeoDataFrame) -> Set[str]:
        return set(
            list(
                map(
                    lambda x: x.geom_type,
                    input_gdf[self.__GEOMETRY_FIELD_NAME].tolist(),
                )
            )
        )

    # def push_layer_to_map(self, layer: "Layer"):
    #
    #     if layer.geom_type == BokehGeomTypes.POINT:
    #         bokeh_container = self.add_points(layer)
    #     if layer.geom_type == BokehGeomTypes.LINESTRINGS:
    #         bokeh_container = self.add_lines(layer)
    #     if layer.geom_type == BokehGeomTypes.POLYGONS:
    #         bokeh_container = self.add_polygons(layer)
    #     else:
    #         raise ErrorGdf2Bokeh("It should not happened")
    #     return bokeh_container

    def refresh_existing_layer(self, layer_settings: dict) -> dict:
        """
        To return a dict to update the data of an existing bokeh layer container

        :return: ColumnDataSource data
        :rtype: dict
        """
        # used also if input gdf is empty
        return dict(self._format_gdf_features_to_bokeh(layer_settings["input_gdf"]).data)

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
    
    @staticmethod
    def __convert_gdf_to_bokeh_data(input_gdf: gpd.GeoDataFrame, get_gdf_structure: bool = False) -> ColumnDataSource:

        if get_gdf_structure:
            input_gdf = input_gdf.head(1)

        bokeh_data = ColumnDataSource(
            {
                **{
                    "x": input_gdf["geometry"]
                    .apply(lambda x: geometry_2_bokeh_format(x, "x"))
                    .tolist(),
                    "y": input_gdf["geometry"]
                    .apply(lambda x: geometry_2_bokeh_format(x, "y"))
                    .tolist(),
                },
                **{
                    column: input_gdf[column].to_list()
                    for column in input_gdf.columns
                    if column != "geometry"
                },
            }
        )
        return bokeh_data

    def _format_gdf_features_to_bokeh(self, input_gdf: gpd.GeoDataFrame | pd.DataFrame) -> ColumnDataSource:
        """
        To build the bokeh data input from a GeoDataframe.

        :param input_gdf: your input [Geo]Dataframe
        :return: the bokeh data input
        :rtype: ColumnDataSource
        """
        bokeh_data = self.__convert_gdf_to_bokeh_data(input_gdf)
        return bokeh_data
