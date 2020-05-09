import geopandas as gpd
import random
import pandas as pd
from shapely.geometry import Point
import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.models import Slider
from bokeh_for_map import BokehForMap

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.layouts import row


class RandonPointsGenerator:
    __POINTS_CREATE = []

    def __init__(self, bounds, points_number):
        self._x_min, self._y_min, self._x_max, self._y_max = bounds
        self._points_number = points_number

        self.__build_points()

    def __build_points(self):
        points_created = 0
        while points_created < self._points_number:
            x = random.uniform(self._x_min, self._x_max)
            y = random.uniform(self._y_min, self._y_max)
            self.__POINTS_CREATE.append({
                "id": points_created,
                "geometry": Point(x, y)
            })
            points_created += 1

    @property
    def to_gdf(self):
        df = pd.DataFrame(self.__POINTS_CREATE)
        geometry = df["geometry"]
        properties = df["id"]
        return gpd.GeoDataFrame(
            properties,
            geometry=geometry
        )


class MyMap(BokehForMap):

    def __init__(self, input_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_data = input_data

    def plot(self):
        self.prepare_data()
        self.slider_widget()

        self._map_layout()

    def prepare_data(self):

        # here we get the data structure to plot and empty points layer. slider widget will fill it
        self._points_input = self.get_structure_features(self._input_data)
        self.add_points(self._points_input, fill_color="black", legend="points")

    def slider_widget(self):
        min_value = min(self._input_data["value"])
        max_value = max(self._input_data["value"])
        self._slider_widget = Slider(start=min_value, end=max_value, value=min_value, step=1, title="my slider")
        self._slider_widget.on_change('value', self.__slider_update)

    def __slider_update(self, attrname, old, new):
        input_data_filtered = self._input_data.loc[self._input_data["value"] == self._slider_widget.value]
        self._points_input.data = dict(self.format_features(input_data_filtered).data)

    def _map_layout(self):
        layout = column(
            row(self.figure),
            row(self._slider_widget),
        )
        curdoc().add_root(layout)
        curdoc().title = "My SandBox"


bounds = [0, 0, 50, 50]
random_points = RandonPointsGenerator(bounds, 50).to_gdf
random_points["value"] = np.random.randint(1, 6, random_points.shape[0])
MyMap(random_points, title="My beautiful map", width=640, height=800).plot()
