import geopandas as gpd
import random
import pandas as pd
from shapely.geometry import Point
import numpy as np

from bokeh.models import Slider
from gdf2bokeh import Gdf2Bokeh

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.layouts import row


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

    def __init__(self, input_layer_settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_layer_settings = input_layer_settings

        self._start_value = 1

    def plot(self):
        self.prepare_data()
        self.slider_widget()

        self._map_layout()

    def prepare_data(self):
        input_data = self._input_layer_settings["input_gdf"]
        input_data_filtered = input_data.loc[input_data["value"] == self._start_value]
        layer_filtered = {**self._input_layer_settings, "input_gdf": input_data_filtered}
        self.push_layer_to_map(layer_filtered)

    def slider_widget(self):
        input_data = self._input_layer_settings["input_gdf"]
        max_value = max(input_data["value"]) + 2
        self._slider_widget = Slider(start=self._start_value, end=max_value, value=self._start_value, step=1, title="my slider")
        self._slider_widget.on_change('value', self.__slider_update)

    def __slider_update(self, attrname, old_value, new_value):
        input_data = self._input_layer_settings["input_gdf"]
        input_data_filtered = input_data.loc[input_data["value"] == new_value]
        layer_filtered = {**self._input_layer_settings, "input_gdf": input_data_filtered}
        self.get_bokeh_layer_containers[layer_filtered["legend"]].layers = self.refresh_existing_layer(layer_filtered)

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

layer_settings = {
    "input_gdf": random_points,
    "fill_color": "red",
    "size": 10,
    "legend": "my points"
}

MyMapBokeh(
    layer_settings,
    title="My beautiful map",
    width=640,
    height=800,
    x_range=(bounds[0], bounds[2]),
    y_range=(bounds[1], bounds[-1]),
    background_map_name="STAMEN_TONER"
).plot()
