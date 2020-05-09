from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import HoverTool



from bokeh_for_map.helpers.geometry import geometry_2_bokeh_format

from bokeh_for_map.helpers.settings import expected_node_style
from bokeh_for_map.helpers.settings import map_background_providers

import geopandas as gpd

class BokehForMap:

    __DEFAULT_FIELD_BOKEH_DATA_FORMAT = {
        "x": [],
        "y": []
    }

    def __init__(self, title="My empty Map", width=800, height=600, x_range=None, y_range=None, background_map_name="CARTODBPOSITRON"):
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

        """
        super().__init__()

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

    def _add_background_map(self, background_map_name):
        assert background_map_name in map_background_providers.keys(), f"Use one of these background map : {', '.join(map_background_providers)}"
        self.figure.add_tile(map_background_providers[background_map_name])

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

    def __convert_gdf_to_bokeh_data(self, features, only_one_feature=False):
        assert isinstance(features, gpd.GeoDataFrame), "use a geodataframe please"
        if only_one_feature:
            features = features.head(1)

        bokeh_data = ColumnDataSource({
            **{
                "x": features['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'x')).tolist(),
                "y": features['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'y')).tolist(),

            },
            **{
                column: features[column].to_list()
                for column in features.columns
                if column != "geometry"
            }
        })
        return bokeh_data

    def format_gdf_features_to_bokeh(self, features):
        """
        To build the bokeh data input from a geodataframe.

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :return: the bokeh data input
        :rtype: ColumnDataSource
        """
        assert isinstance(features, gpd.GeoDataFrame), "use a geodataframe please"
        assert "geometry" in features.columns

        bokeh_data = self.__convert_gdf_to_bokeh_data(features)
        return bokeh_data

    def get_bokeh_structure_from_gdf_features(self, features):
        """
        To build the bokeh data structure from a geodataframe.

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :return: the bokeh data structure
        :rtype: ColumnDataSource
        """
        assert isinstance(features, gpd.GeoDataFrame), "use a geodataframe please"

        bokeh_data = self.__convert_gdf_to_bokeh_data(features, True)
        return ColumnDataSource(data=dict.fromkeys(bokeh_data.column_names, []))

    def add_lines(self, features, legend, color="blue", line_width=2):
        """
        To add a lines layer on bokeh Figure

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param color: color value
        :type color: str
        :param line_width: line width
        :type line_width: int
        """
        assert isinstance(features, ColumnDataSource)
        rendered = self.figure.multi_line(
            xs="x",
            ys="y",
            legend_label=legend,
            line_color=color,
            line_width=line_width,
            source=features,
        )
        self._set_tooltip_from_features(features, rendered)

    def add_points(self, features, legend, fill_color="red", size=4, style="circle"):
        """
        To add a points layer on bokeh Figure

        :param features: ColumnDataSource
        :type features: ColumnDataSource
        :param legend: layer name
        :type legend: str
        :param color: color value
        :type color: str
        :param size: node size
        :type size: int
        :param style: node style, check expected_node_style variable
        :type style: str
        """
        assert style in expected_node_style, f"{style} not supported. Choose one of them : {', '.join(expected_node_style)}"
        assert isinstance(features, ColumnDataSource)
        rendered = getattr(self.figure, style)(
            x="x",
            y="y",
            color=fill_color,
            size=size,
            legend_label=legend,
            source=features,
        )
        self._set_tooltip_from_features(features, rendered)

    def add_polygons(self, features, legend, fill_color="red"):
        """
        To add a polygons layer on bokeh Figure

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param fill_color: color value
        :type fill_color: str
        """
        assert isinstance(features, ColumnDataSource)
        rendered = self.figure.multi_polygons(
            xs="x",
            ys="y",
            legend_label=legend,
            fill_color=fill_color,
            source=features,
        )
        self._set_tooltip_from_features(features, rendered)

