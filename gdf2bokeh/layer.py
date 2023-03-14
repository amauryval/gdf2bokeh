from enum import Enum
from typing import List
from typing import Tuple

import geopandas as gpd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.renderers import GlyphRenderer

from bokeh.models import HoverTool

from gdf2bokeh.geometry import geometry_2_bokeh_format


class GeomTypeError(Exception):
    pass


class GeomTypes(set, Enum):
    LINESTRINGS = {"LineString", "MultiLineString"}
    POLYGONS = {"Polygon", "MultiPolygon"}
    POINT = {"Point"}
    MULTIPOINT = {"MultiPoint"}

    @staticmethod
    def has_value(item: set):
        for enum in GeomTypes.__members__.values():
            if item.issubset(enum):
                return enum
        raise GeomTypeError(f"{item} not supported")


class LayerCore:
    title = None
    _data = None
    _geom_type = None
    _data_source = None
    _style_parameters = None

    __GEOMETRY_FIELD_NAME: str = "geometry"
    _DEFAULT_EPSG: int = 3857

    def __init__(self, title: str, data: gpd.GeoDataFrame, from_epsg: int, **style_parameters):
        self._data_source = ColumnDataSource()  # self.data_source_structure(data)
        self._from_epsg = from_epsg
        self.title = title
        self.data = data
        self._style_parameters = style_parameters

    def render(self, figure_obj: figure):
        raise NotImplemented

    @property
    def geom_type(self) -> GeomTypes:
        return self._geom_type

    @property
    def data(self) -> gpd.GeoDataFrame:
        return self._data

    @data.setter
    def data(self, data: gpd.GeoDataFrame) -> None:
        self._data = data
        if self._from_epsg != self._DEFAULT_EPSG:
            self._data = self._data.to_crs(f"epsg:{self._DEFAULT_EPSG}")
        # data is updated, so let's go to refresh the data_source container linked to bokeh layer
        self.refresh_data_source()

    def refresh_data_source(self):
        raise NotImplemented

    def data_source_structure(self, data: gpd.geodataframe) -> ColumnDataSource:
        """
        To build the bokeh data structure from a GeoDataframe.
        """
        data = data.head(1)
        data = self._format_gdf_features_to_bokeh(data)
        return ColumnDataSource(data=dict.fromkeys(data.column_names, []))

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

    def _set_tooltip(self, figure_obj: figure, rendered: GlyphRenderer) -> None:
        column_tooltip = self.__build_column_tooltip(self._data_source)
        figure_obj.add_tools(
            HoverTool(tooltips=column_tooltip, renderers=[rendered], mode="mouse")
        )

    @staticmethod
    def __build_column_tooltip(features_column_data_source: ColumnDataSource) -> List[Tuple[str, str]]:
        columns = list(filter(lambda x: x not in ["x", "y"], features_column_data_source.data.keys()))
        return list(
            zip(map(lambda x: str(x.upper()), columns), map(lambda x: f"@{x}", columns))
        )


class PointLayer(LayerCore):
    _geom_type = GeomTypes.POINT
    _DEFAULT_STYLE = "circle"

    def __init__(self, title: str, data: gpd.GeoDataFrame, from_epsg: int, **style_parameters) -> None:
        super().__init__(title=title, data=data, from_epsg=from_epsg, **style_parameters)

    def refresh_data_source(self):
        self._data_source.data = dict(self._format_gdf_features_to_bokeh(self.data).data)

    def render(self, figure_obj: figure) -> None:
        """render the bokeh object"""
        render = getattr(figure_obj, self._DEFAULT_STYLE)(
            x="x", y="y", source=self._data_source, legend_label=self.title, **self._style_parameters
        )
        self._set_tooltip(figure_obj, render)


class MultiPointLayer(PointLayer):
    def __init__(self, title: str, data: gpd.GeoDataFrame, from_epsg: int, **style_parameters) -> None:
        data = data.explode(index_parts=False)
        super().__init__(title=title, data=data, from_epsg=from_epsg, **style_parameters)


class LinestringLayer(LayerCore):
    _geom_type = GeomTypes.LINESTRINGS

    def __init__(self, title: str, data: gpd.GeoDataFrame, from_epsg: int, **style_parameters) -> None:
        data = self._clean_lines_from_gdf(data)
        super().__init__(title=title, data=data, from_epsg=from_epsg, **style_parameters)

    def refresh_data_source(self):
        # go to check the multilinestring continuity, because the bokeh format cannot display a multilinestring
        # containing a discontinuity. We'll convert the objet into linestring if needed.
        data = self._clean_lines_from_gdf(self.data)
        self._data_source.data = dict(self._format_gdf_features_to_bokeh(data).data)

    def render(self, figure_obj: figure) -> None:
        """render the bokeh object"""
        render = figure_obj.multi_line(
            xs="x", ys="y", source=self._data_source, legend_label=self.title, **self._style_parameters
        )
        self._set_tooltip(figure_obj, render)

    @staticmethod
    def _clean_lines_from_gdf(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        return input_gdf.explode(index_parts=False)


class PolygonLayer(LayerCore):
    _geom_type = GeomTypes.POLYGONS

    def __init__(self, title: str, data: gpd.GeoDataFrame, from_epsg: int, **style_parameters) -> None:
        super().__init__(title=title, data=data, from_epsg=from_epsg, **style_parameters)

    def refresh_data_source(self):
        self._data_source.data = dict(self._format_gdf_features_to_bokeh(self.data).data)

    def render(self, figure_obj: figure) -> None:
        """render the bokeh object"""
        render = figure_obj.multi_polygons(
            xs="x", ys="y", source=self._data_source, legend_label=self.title, **self._style_parameters
        )
        self._set_tooltip(figure_obj, render)
