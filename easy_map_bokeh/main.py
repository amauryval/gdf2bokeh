import geopandas as gpd


from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from bokeh.models import HoverTool
from bokeh.palettes import brewer

from easy_map_bokeh.helpers.geometry import geometry_2_bokeh_format

from easy_map_bokeh.helpers.settings import expected_node_style
from easy_map_bokeh.helpers.settings import map_background_providers
from easy_map_bokeh.helpers.settings import default_attributes

from easy_map_bokeh.helpers.settings import geometry_compatibility
from easy_map_bokeh.helpers.settings import linestrings_type_compatibility
from easy_map_bokeh.helpers.settings import polygons_type_compatibility
from easy_map_bokeh.helpers.settings import point_type_compatibility


class ErrorEasyMapBokeh(Exception):
    pass


class EasyMapBokeh:

    __GEOMETRY_FIELD_NAME = "geometry"
    __DEFAULT_EPSG = 3857
    __BREWER_COLORS = brewer["Set3"][7]

    def __init__(self, title="My empty Map", width=800, height=600, x_range=None, y_range=None, background_map_name="CARTODBPOSITRON", layers=None):
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
        :param layers: list of geodataframe
        :type layers: list(geopandas.GeoDataFrame)
        """
        super().__init__()

        self.__BOKEH_LAYER_CONTAINERS = {}

        self.figure = figure(
            title=title,
            output_backend="webgl",
            tools="pan,wheel_zoom,box_zoom,reset,save",
            x_range=x_range,
            y_range=y_range
        )

        self.figure.plot_width = width
        self.figure.plot_height = height

        self._add_background_map(background_map_name)

        self._layers_configuration = layers
        if layers is not None:
            self.__add_layers()

    @property
    def get_bokeh_layer_containers(self):
        """
        To get all the bokeh layer containers in order to create dynamic layer (with slider for example)

        :return: bokeh layer container
        :rtype: dict
        """
        return self.__BOKEH_LAYER_CONTAINERS

    def get_bokeh_structure_from_gdf(self, features):
        """
        To build the bokeh data structure from a geodataframe.

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :return: the bokeh data structure
        :rtype: bokeh.models.ColumnDataSource
        """
        assert isinstance(features, gpd.GeoDataFrame), "use a geodataframe please"

        bokeh_data = self.__convert_gdf_to_bokeh_data(features, get_gdf_structure=True)
        return ColumnDataSource(data=dict.fromkeys(bokeh_data.column_names, []))

    def __legend_settings(self):
        # interactive legend
        self.figure.legend.click_policy = "hide"

    def __reprojection(self, input_data):
        expected_epsg = f"epsg:{self.__DEFAULT_EPSG}"
        if input_data.crs != expected_epsg:

            return input_data.to_crs(expected_epsg)

        return input_data

    def add_lines(self, input_gdf, legend, **kwargs):
        """
        To add a lines layer on bokeh Figure (LineString and MultiLineString geometry types supported)

        :param input_gdf: your input geodataframe
        :type input_gdf: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param **kwargs: arguments from bokeh to style the layer
        :type **kwargs: str

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        layer_geom_types = self.__get_geom_types_from_gdf(input_gdf)
        if layer_geom_types.issubset(linestrings_type_compatibility):

            input_data = input_gdf.copy(deep=True)
            input_data = self.__reprojection(input_data)
            bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)

            rendered = self.figure.multi_line(
                xs="x",
                ys="y",
                legend_label=legend,
                source=bokeh_layer_container,
                **kwargs
            )
            self._set_tooltip_from_features(bokeh_layer_container, rendered)
            self.__legend_settings()

            self.__BOKEH_LAYER_CONTAINERS[legend] = bokeh_layer_container
            return bokeh_layer_container

        else:
            raise ErrorEasyMapBokeh(
                f"{layer_geom_types} geometry not supported by add_lines() method: only works with {' and '.join(linestrings_type_compatibility)} (layer concerned '{legend}')")

    def add_points(self, input_gdf, legend, style="circle", **kwargs):
        """
        To add a points layer on bokeh Figure  (Point geometry type supported)

        :param input_gdf: ColumnDataSource
        :type input_gdf: bokeh.models.ColumnDataSource
        :param legend: layer name
        :type legend: str
        :param style: node style, check expected_node_style variable
        :type style: str
        :param **kwargs: arguments from bokeh to style the layer
        :type **kwargs: str

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        assert style in expected_node_style, f"{style} not supported. Choose one of them : {', '.join(expected_node_style)}"

        layer_geom_types = self.__get_geom_types_from_gdf(input_gdf)
        if layer_geom_types.issubset(point_type_compatibility):

            input_data = input_gdf.copy(deep=True)
            input_data = self.__reprojection(input_data)
            bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)

            rendered = getattr(self.figure, style)(
                x="x",
                y="y",
                legend_label=legend,
                source=bokeh_layer_container,
                **kwargs
            )
            self._set_tooltip_from_features(bokeh_layer_container, rendered)
            self.__legend_settings()

            self.__BOKEH_LAYER_CONTAINERS[legend] = bokeh_layer_container

            return bokeh_layer_container

        else:
            raise ErrorEasyMapBokeh(
                f"{layer_geom_types} geometry not supported by add_points() method: only works with {' and '.join(point_type_compatibility)} (layer concerned '{legend}')")

    def add_polygons(self, input_gdf, legend, **kwargs):
        """
        To add a polygons layer on bokeh Figure (Polygon and MultiPolygon geometry type supported)

        :param input_gdf: your input geodataframe
        :type input_gdf: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param **kwargs: arguments from bokeh to style the layer
        :type **kwargs: str

        :return: the bokeh layer container (can be used to create dynamic (with slider) layer
        :rtype: bokeh.models.ColumnDataSource
        """

        layer_geom_types = self.__get_geom_types_from_gdf(input_gdf)
        if layer_geom_types.issubset(polygons_type_compatibility):

            input_data = input_gdf.copy(deep=True)
            input_data = self.__reprojection(input_data)
            bokeh_layer_container = self._format_gdf_features_to_bokeh(input_data)

            rendered = self.figure.multi_polygons(
                xs="x",
                ys="y",
                legend_label=legend,
                source=bokeh_layer_container,
                **kwargs
            )
            self._set_tooltip_from_features(bokeh_layer_container, rendered)
            self.__legend_settings()

            self.__BOKEH_LAYER_CONTAINERS[legend] = bokeh_layer_container
            return bokeh_layer_container

        else:
            raise ErrorEasyMapBokeh(
                f"{layer_geom_types} geometry not supported by add_polygons() method: only works with {' and '.join(polygons_type_compatibility)} (layer concerned '{legend}')")

    def _add_background_map(self, background_map_name):
        assert background_map_name in map_background_providers.keys(), f"Use one of these background map : {', '.join(map_background_providers)}"
        self.figure.add_tile(map_background_providers[background_map_name])

    def __get_geom_types_from_gdf(self, input_gdf):
        return set(list(map(lambda x: x.geom_type, input_gdf[self.__GEOMETRY_FIELD_NAME].tolist())))

    def __add_layers(self):
        assert isinstance(self._layers_configuration , list), "layers arg is not a list"

        for layer_settings in self._layers_configuration:
            assert isinstance(layer_settings, dict), "use a dict please"
            layer_geom_types = self.__get_geom_types_from_gdf(layer_settings["input_gdf"])
            assert default_attributes.issubset(set(layer_settings.keys())), f"These attributes are required: {' ,'.join(default_attributes)}"

            if len(layer_geom_types) > 0:
                compatibility_checked = list(filter(lambda x: layer_geom_types.issubset(x) or layer_geom_types == x, geometry_compatibility))

                if len(compatibility_checked) == 1:

                    if layer_geom_types.issubset(point_type_compatibility):
                        self.add_points(**layer_settings)

                    elif layer_geom_types.issubset(linestrings_type_compatibility):
                        self.add_lines(**layer_settings)

                    elif layer_geom_types.issubset(polygons_type_compatibility):
                        self.add_polygons(**layer_settings)

                else:
                    raise ErrorEasyMapBokeh(f"{layer_geom_types} geometry have to be split by geometry types (layer concerned '{layer_settings['legend']}')")
            else:
                raise ErrorEasyMapBokeh(f"Your geodataframe may not have geometry features (layer concerned '{layer_settings['legend']}')")


    def _set_tooltip_from_features(self, features, rendered):
        assert isinstance(features, ColumnDataSource)
        column_tooltip = self.__build_column_tooltip(features)
        self.figure.add_tools(HoverTool(
            tooltips=column_tooltip,
            renderers=[rendered],
            mode="mouse"
        ))

    def __build_column_tooltip(self, features):
        columns = list(filter(lambda x: x not in ["x", "y"], features.data.keys()))
        return list(zip(map(lambda x: str(x.upper()), columns), map(lambda x: f"@{x}", columns)))

    def __convert_gdf_to_bokeh_data(self, input_gdf, get_gdf_structure=False):
        assert isinstance(input_gdf, gpd.GeoDataFrame), f"use a geodataframe please => found {type(input_gdf)}"
        if get_gdf_structure:
            input_gdf = input_gdf.head(1)

        bokeh_data = ColumnDataSource({
            **{
                "x": input_gdf['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'x')).tolist(),
                "y": input_gdf['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'y')).tolist(),

            },
            **{
                column: input_gdf[column].to_list()
                for column in input_gdf.columns
                if column != "geometry"
            }
        })
        return bokeh_data

    def _format_gdf_features_to_bokeh(self , input_gdf):
        """
        To build the bokeh data input from a geodataframe.

        :param input_gdf: your input geodataframe
        :type input_gdf: geopandas.GeoDataFrame
        :return: the bokeh data input
        :rtype: ColumnDataSource
        """
        assert isinstance(input_gdf, gpd.GeoDataFrame), f"use a geodataframe please => found {type(input_gdf)}"
        assert "geometry" in input_gdf.columns

        bokeh_data = self.__convert_gdf_to_bokeh_data(input_gdf)
        return bokeh_data


