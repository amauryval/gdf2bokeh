from enum import Enum
from typing import List
from typing import Tuple

import geopandas as gpd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.renderers import GlyphRenderer

from bokeh.models import HoverTool

from gdf2bokeh.geometry import geometry_2_bokeh_format
from gdf2bokeh.geometry import check_multilinestring_continuity


class GeomTypeError(Exception):
    pass


class GeomTypes(set, Enum):
    LINESTRINGS = {"LineString", "MultiLineString"}
    POLYGONS = {"Polygon", "MultiPolygon"}
    POINT = {"Point"}
    MULTIPOINT = {"MultiPoint"}  # TODO support it

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
    _style_parameters = None

    __GEOMETRY_FIELD_NAME: str = "geometry"
    _DEFAULT_EPSG: int = 3857

    def __init__(self, title: str, data: gpd.GeoDataFrame, **style_parameters):
        self.title = title
        self._data = data
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
        expected_epsg = f"epsg:{self._DEFAULT_EPSG}"
        if data.crs != expected_epsg:
            data = self._data.to_crs(expected_epsg)
        self._data = data

    @property
    def data_source(self):
        raise NotImplemented

    @property
    def data_source_structure(self) -> ColumnDataSource:
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

    def _set_tooltip(self, figure_obj: figure, rendered: GlyphRenderer) -> None:
        column_tooltip = self.__build_column_tooltip(self.data_source)
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

    def __init__(self, title: str, data: gpd.GeoDataFrame, **style_parameters) -> None:
        super().__init__(title=title, data=data, **style_parameters)

    @property
    def data_source(self) -> ColumnDataSource:
        return self._format_gdf_features_to_bokeh(self.data)

    def render(self, figure_obj: figure) -> None:
        """render the bokeh object"""
        render = getattr(figure_obj, self._DEFAULT_STYLE)(
            x="x", y="y", source=self.data_source, legend_label=self.title, **self._style_parameters
        )
        self._set_tooltip(figure_obj, render)


class LinestringLayer(LayerCore):
    _geom_type = GeomTypes.LINESTRINGS

    def __init__(self, title: str, data: gpd.GeoDataFrame, **style_parameters) -> None:
        super().__init__(title=title, data=data, **style_parameters)

    @property
    def data_source(self) -> ColumnDataSource:
        # go to check the multilinestring continuity, because the bokeh format cannot display a multilinestring
        # containing a discontinuity. We'll convert the objet into linestring if needed.
        data = self.__post_proc_multilinestring_gdf(self.data)
        return self._format_gdf_features_to_bokeh(data)

    def render(self, figure_obj: figure) -> None:
        """render the bokeh object"""
        render = figure_obj.multi_line(
            xs="x", ys="y", source=self.data_source, **self._style_parameters
        )
        self._set_tooltip(figure_obj, render)


class PolygonLayer(LayerCore):
    _geom_type = GeomTypes.POLYGONS

    def __init__(self, title: str, data: gpd.GeoDataFrame, **style_parameters) -> None:
        super().__init__(title=title, data=data, **style_parameters)

    @property
    def data_source(self) -> ColumnDataSource:
        return self._format_gdf_features_to_bokeh(self.data)

    def render(self, figure_obj: figure) -> None:
        """render the bokeh object"""
        render = figure_obj.multi_polygons(
            xs="x", ys="y", source=self.data_source, **self._style_parameters
        )
        self._set_tooltip(figure_obj, render)
