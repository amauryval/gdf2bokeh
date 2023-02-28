from typing import Dict

import geopandas as gpd
import random
import pandas as pd
from shapely.geometry import Point
import numpy as np

from bokeh.models import Slider
from gdf2bokeh import Gdf2Bokeh, LayerCore

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.plotting import show


class RandomPointsGenerator:
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
            geometry=geometry,
            crs='EPSG:3857'
        )




class MyMapBokeh(Gdf2Bokeh):
    _start_value = 1

    _slider_widget = None

    def __init__(self, layer: Dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layer = layer
        self._bokeh_layer = self.prepare_layer(self._start_value)

    def plot(self):
        self.slider_widget()
        self._map_layout()

    def prepare_layer(self, filter_value: int) -> LayerCore:
        input_data_filtered = self._layer["data"].loc[self._layer["data"]["value"] == filter_value]
        self.add_layer_from_geodataframe(self._layer["title"], input_data_filtered, size=self._layer["size"],
                                         fill_color=self._layer["fill_color"], line_color=self._layer["line_color"])
        self.add_layers_on_maps()

        return self._layers[self._layer["title"]]

    def slider_widget(self):
        """Set the slider widget"""
        input_data = self._layer["data"]
        max_value = max(input_data["value"])
        self._slider_widget = Slider(start=self._start_value, end=max_value, value=self._start_value, step=1, title="my slider")
        self._slider_widget.on_change('value', self.__slider_update)

    def __slider_update(self, attrname, old_value, new_value):
        input_data_filtered = self._layer["data"].loc[self._layer["data"]["value"] == new_value]
        print(input_data_filtered.shape)
        self._bokeh_layer.data = input_data_filtered

    def _map_layout(self):
        layout = column(
            row(self.figure),
            row(self._slider_widget),
        )
        curdoc().add_root(layout)
        curdoc().title = "My SandBox"

bounds = (-604158.2716, 5312679.2139, 1081125.3281, 6633511.0627)
random_points = RandomPointsGenerator(bounds, 50).to_gdf
random_points["value"] = np.random.randint(1, 6, random_points.shape[0])

layer = {
    "title": "Points",
    "data": random_points,
    "size": 10,
    "fill_color": "red",
    "line_color": "blue"
}


map_session = MyMapBokeh(layer)
map_session.plot()


