from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.tile_providers import get_provider
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import HoverTool

from bfm.helpers.geometry import geometry_2_bokeh_format

from bfm.helpers.settings import expected_node_style


class BokehForMap:

    def __init__(self, title="My empty Map", width=800, height=600, background_map=CARTODBPOSITRON):
        super().__init__()

        self.figure = figure(
            title=title,
            output_backend="webgl",
            tools="box_select,pan,wheel_zoom,box_zoom,reset,save"
        )

        self.figure.plot_width = width
        self.figure.plot_height = height

        self._add_background_map(background_map)

    def _add_background_map(self, map_name_object):
        tile_provider = get_provider(map_name_object)
        self.figure.add_tile(tile_provider)

    def _set_layer_parameters(self, renderer, features):
        self.figure.legend.click_policy = "hide"

        column_tooltip = self.__build_column_tooltip(features)
        self.figure.add_tools(HoverTool(
            tooltips=column_tooltip,
            renderers=[renderer],
            mode="mouse"
        ))

    def _format_features(self, feature):
        return ColumnDataSource({
            **{
                "x": feature['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'x')).tolist(),
                "y": feature['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'y')).tolist(),
            },
            **{
                column: feature[column].to_list()
                for column in feature.columns
                if column != "geometry"
            }
        })

    def add_lines(self, features, legend, color="blue", line_width=2):
        source_data = self._format_features(features)
        rendered = self.figure.line(
            x="x",
            y="y",
            legend_label=legend,
            line_color=color,
            line_width=line_width,
            source=source_data,
        )
        self._set_layer_parameters(rendered, features)

    def add_points(self, features, legend, fill_color="red", size=4, style="circle"):
        assert style in expected_node_style, f"{style} not supported. Choose one of them : {', '.join(expected_node_style)}"

        # MultiPoints are tricky !
        rendered = getattr(self.figure, style)(
            x="x",
            y="y",
            color=fill_color,
            size=size,
            legend_label=legend,
            source=self._format_features(features)
        )
        self._set_layer_parameters(rendered, features)

    def add_polygons(self, feature, legend, fill_color="red"):
        rendered = self.figure.multi_polygons(
            xs="x",
            ys="y",
            legend_label=legend,
            fill_color=fill_color,
            source=self._format_features(feature),
        )
        self._set_layer_parameters(rendered, feature)

    def __build_column_tooltip(self, features):
        columns_filtered = list(filter(lambda x: x != "geometry", features.columns))
        return list(zip(map(lambda x: str(x.upper()), columns_filtered), map(lambda x: f"@{x}", columns_filtered)))
