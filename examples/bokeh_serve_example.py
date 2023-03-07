from typing import Dict

from bokeh.models import Slider

from examples.common import build_data
from gdf2bokeh import Gdf2Bokeh, LayerCore

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.layouts import row


class MyMapBokeh(Gdf2Bokeh):
    _start_value = 1

    _slider_widget = None

    def __init__(self, layer: Dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._layer = layer
        self._bokeh_layer = self.prepare_layer(self._start_value)

    def plot(self) -> None:
        self.slider_widget()
        self._map_layout()

    def prepare_layer(self, filter_value: int) -> LayerCore:
        input_data_filtered = self._layer["data"].loc[self._layer["data"]["value"] == filter_value]
        self.add_layer_from_geodataframe(self._layer["title"], input_data_filtered, from_epsg=self._layer["from_epsg"],
                                         size=self._layer["size"], fill_color=self._layer["fill_color"],
                                         line_color=self._layer["line_color"])
        self.add_layers_on_maps()

        return self._layers[self._layer["title"]]

    def slider_widget(self) -> None:
        """Set the slider widget"""
        input_data = self._layer["data"]
        max_value = max(input_data["value"])
        self._slider_widget = Slider(start=self._start_value, end=max_value, value=self._start_value, step=1,
                                     title="my slider")
        self._slider_widget.on_change('value', self.__slider_update)

    def __slider_update(self, attrname, old_value, new_value) -> None:
        input_data_filtered = self._layer["data"].loc[self._layer["data"]["value"] == new_value]
        print(input_data_filtered.shape)
        self._bokeh_layer.data = input_data_filtered

    def _map_layout(self) -> None:
        layout = column(
            row(self.figure),
            row(self._slider_widget),
        )
        curdoc().add_root(layout)
        curdoc().title = "My SandBox"


if __name__ == '__main__':

    layer = {
        "title": "Points",
        "data": build_data(),
        "from_epsg": 2154,
        "size": 10,
        "fill_color": "red",
        "line_color": "blue"
    }

    map_session = MyMapBokeh(layer)
    map_session.plot()
