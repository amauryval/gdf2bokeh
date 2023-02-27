from typing import List
from typing import Optional
from typing import Dict
from typing import Set
from typing import Tuple
from typing import Union
from typing import Any

import geopandas as gpd
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.renderers import GlyphRenderer

from bokeh.models import HoverTool
from bokeh.palettes import brewer

from gdf2bokeh.helpers.geometry import wkt_to_gpd
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


class Gdf2Bokeh:

    __GEOMETRY_FIELD_NAME: str = "geometry"
    __DEFAULT_EPSG: int = 3857
    __BREWER_COLORS: List = brewer["Set3"][7]

    def __init__(
        self,
        title: str = "My empty Map",
        width: int = 800,
        height: int = 600,
        background_map_name: str = "CARTODBPOSITRON",
        layers: Optional[List[Dict[str, Union[str, Any]]]] = None,
    ) -> None:
        """
        :param title: figure title
        :type title: str
        :param width: width value
        :type width: int
        :param height: height value
        :type height: int
        :param x_range: x range to fix x canvas axe
        :type x_range: tuple of 2 floats, default None
        :param y_range: y range to fix y canvas axe
        :type y_range: tuple of 2 floats, default None
        :param background_map_name: background map name
        :type background_map_name: str
        :param layers: list of dict with input data: (input_gdf or input_wkt) and legend, and bokeh style properties
        :type layers: lit of dict
        """
        super().__init__()

        # TODO create a getter, keys should be unique
        self.__BOKEH_LAYER_CONTAINERS: Dict = {}

        self.figure = figure(
            title=title,
            output_backend="webgl",
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )

        self.figure.width = width
        self.figure.height = height

        self._add_background_map(background_map_name)

        self._layers_configuration = layers
        if layers is not None:
            self.__add_layers()

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

    def add_lines(
        self, input_gdf: gpd.GeoDataFrame, legend: str, **kwargs
    ) -> ColumnDataSource:
        """
        To add a lines layer on bokeh Figure (LineString and MultiLineString geometry types supported)

        :param input_gdf: your input GeoDataframe
        :type input_gdf: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param kwargs: arguments from bokeh to style the layer
        :type kwargs: str

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        layer_geom_types = self.__get_geom_types_from_gdf(input_gdf)
        if layer_geom_types.issubset(linestrings_type_compatibility):

            input_data = self.__post_proc_input_gdf(input_gdf)
            # go to check the multilinestring continuity, because the bokeh format cannot display a multilinestring
            # containing a discontinuity. We'll convert the objet into linestring if needed.
            input_data = self.__post_proc_multilinestring_gdf(input_data)
            bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)
            kwargs = self.__check_is_legend_field_exists_in_input_gdf(
                input_data, legend, kwargs
            )

            rendered = self.figure.multi_line(
                xs="x", ys="y", source=bokeh_layer_container, **kwargs
            )
            self._set_tooltip_from_features(bokeh_layer_container, rendered)
            self.__legend_settings()

            self.__BOKEH_LAYER_CONTAINERS[legend] = bokeh_layer_container
            return bokeh_layer_container

        else:
            raise ErrorGdf2Bokeh(
                f"{layer_geom_types} geometry not supported by add_lines() method: only works with "
                f"{' and '.join(linestrings_type_compatibility)} (layer concerned '{legend}')"
            )

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

    def add_points(self, input_gdf: gpd.GeoDataFrame, legend: str, style: str = "circle", **kwargs) -> ColumnDataSource:
        """
        To add a points layer on bokeh Figure  (Point geometry type supported)

        :param input_gdf: ColumnDataSource
        :type input_gdf: bokeh.models.ColumnDataSource
        :param legend: layer name
        :type legend: str
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

        layer_geom_types = self.__get_geom_types_from_gdf(input_gdf)
        if layer_geom_types.issubset(point_type_compatibility):

            input_data = self.__post_proc_input_gdf(input_gdf)
            bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)
            kwargs = self.__check_is_legend_field_exists_in_input_gdf(
                input_data, legend, kwargs
            )

            rendered = getattr(self.figure, style)(
                x="x", y="y", source=bokeh_layer_container, **kwargs
            )
            self._set_tooltip_from_features(bokeh_layer_container, rendered)
            self.__legend_settings()

            self.__BOKEH_LAYER_CONTAINERS[legend] = bokeh_layer_container

            return bokeh_layer_container

        else:
            raise ErrorGdf2Bokeh(
                f"{layer_geom_types} geometry not supported by add_points() method: only works with "
                f"{' and '.join(point_type_compatibility)} (layer concerned '{legend}')"
            )

    @staticmethod
    def __check_is_legend_field_exists_in_input_gdf(input_data: gpd.GeoDataFrame, legend: str, kwargs) -> Dict:
        if legend in input_data.columns.to_list():
            kwargs["legend_field"] = legend
        else:
            kwargs["legend_label"] = legend

        return kwargs

    def add_polygons(self, input_gdf: gpd.GeoDataFrame, legend: str, **kwargs) -> ColumnDataSource:
        """
        To add a polygons layer on bokeh Figure (Polygon and MultiPolygon geometry type supported)

        :param input_gdf: your input GeoDataframe
        :type input_gdf: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param kwargs: arguments from bokeh to style the layer
        :type kwargs: str

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        layer_geom_types = self.__get_geom_types_from_gdf(input_gdf)
        if layer_geom_types.issubset(polygons_type_compatibility):

            input_data = self.__post_proc_input_gdf(input_gdf)
            bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)
            kwargs = self.__check_is_legend_field_exists_in_input_gdf(
                input_data, legend, kwargs
            )

            rendered = self.figure.multi_polygons(
                xs="x", ys="y", source=bokeh_layer_container, **kwargs
            )
            self._set_tooltip_from_features(bokeh_layer_container, rendered)
            self.__legend_settings()

            self.__BOKEH_LAYER_CONTAINERS[legend] = bokeh_layer_container
            return bokeh_layer_container

        else:
            raise ErrorGdf2Bokeh(
                f"{layer_geom_types} geometry not supported by add_polygons() method: only works with "
                f"{' and '.join(polygons_type_compatibility)} (layer concerned '{legend}')"
            )

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

    def __add_layers(self) -> None:
        assert isinstance(self._layers_configuration, list), "layers arg is not a list"

        for layer_settings in self._layers_configuration:
            _ = self.add_layer(layer_settings)

    def add_layer(self, layer_settings: dict):
        """
        To generate a bokeh container

        :param layer_settings: list of dict with settings: (input_gdf or input_wkt) and legend + bokeh style properties
        :type layer_settings: lit of dict

        :return: the bokeh layer container (can be used to create dynamic (with widgets) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        layer_settings = self.__prepare_input_data(layer_settings)

        # geom type checking
        layer_geom_types = self.__get_geom_types_from_gdf(
            layer_settings["input_gdf"]
        )
        assert default_attributes.issubset(
            set(layer_settings.keys())
        ), f"This attribute is required: {' ,'.join(default_attributes)}"

        if len(layer_geom_types) > 0:

            compatibility_checked = list(filter(
                lambda x: layer_geom_types.issubset(x) or layer_geom_types == x,
                geometry_compatibility
            ))

            if len(compatibility_checked) == 1:
                if layer_geom_types.issubset(point_type_compatibility):
                    bokeh_container = self.add_points(**layer_settings)
                elif layer_geom_types.issubset(linestrings_type_compatibility):
                    bokeh_container = self.add_lines(**layer_settings)
                elif layer_geom_types.issubset(polygons_type_compatibility):
                    bokeh_container = self.add_polygons(**layer_settings)
                else:
                    raise ErrorGdf2Bokeh("It should not happened :)")
                return bokeh_container

            else:
                raise ErrorGdf2Bokeh(
                    f"{layer_geom_types} geometry have to be split by geometry types (layer concerned '{layer_settings['legend']}')"
                )
        else:
            # means that the input gdf is empty, we are going to refresh the bokeh map container only
            self.refresh_existing_layer(layer_settings)

    def refresh_existing_layer(self, layer_settings: dict) -> dict:
        """

        To return a dict to update the data of an existing bokeh layer container

        :param layer_settings: list of dict with input data: (input_gdf or input_wkt) and legend, and bokeh style properties
        :type layer_settings: lit of dict

        :return: ColumnDataSource data
        :rtype: dict
        """
        # used also if input gdf is empty
        layer_settings = self.__prepare_input_data(layer_settings)
        return dict(self._format_gdf_features_to_bokeh(layer_settings["input_gdf"]).data)

    @staticmethod
    def __prepare_input_data(layer_settings):
        assert isinstance(layer_settings, dict), "use a dict please"
        assert len(input_data_default_attributes.intersection(set(layer_settings.keys()))) == 1,\
            f"One of these input attributes are required: {' ,'.join(input_data_default_attributes)}"

        # compute gdf if needed
        if "input_wkt" in layer_settings:
            layer_settings["input_gdf"] = wkt_to_gpd(layer_settings["input_wkt"])
            del layer_settings["input_wkt"]

        return layer_settings

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
    def __convert_gdf_to_bokeh_data(input_gdf: gpd.GeoDataFrame | pd.DataFrame, get_gdf_structure: bool = False) -> ColumnDataSource:
        assert isinstance(input_gdf, (gpd.GeoDataFrame | pd.DataFrame)), f"use a GeoDataframe please => found {type(input_gdf)}"

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

    def _format_gdf_features_to_bokeh(self, input_gdf: gpd.GeoDataFrame) -> ColumnDataSource:
        """
        To build the bokeh data input from a GeoDataframe.

        :param input_gdf: your input GeoDataframe
        :type input_gdf: geopandas.GeoDataFrame
        :return: the bokeh data input
        :rtype: ColumnDataSource
        """
        assert isinstance(input_gdf,
                          (gpd.GeoDataFrame | pd.DataFrame)), f"use a GeoDataframe please => found {type(input_gdf)}"

        assert "geometry" in input_gdf.columns

        bokeh_data = self.__convert_gdf_to_bokeh_data(input_gdf)
        return bokeh_data
