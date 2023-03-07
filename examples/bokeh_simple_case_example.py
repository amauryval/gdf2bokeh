from examples.common import build_data

from gdf2bokeh import Gdf2Bokeh

from bokeh.plotting import show

if __name__ == '__main__':

    map_session = Gdf2Bokeh()
    map_session.add_layer_from_geodataframe("tutu", build_data(), from_epsg=2154, size=10, fill_color="red",
                                            line_color="blue")
    map_session.add_layers_on_maps()

    show(map_session.figure)
