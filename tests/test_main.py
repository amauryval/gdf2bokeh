import geopandas as gpd

from bokeh_for_map import BokehForMap


def test_bokeh_processing(multipolygons_data):
    width = 640
    height = 800

    my_map = BokehForMap("My beautiful map", width, height)
    bokeh_multipolygons = my_map.format_gdf_features_to_bokeh(multipolygons_data)
    my_map.add_polygons(
        bokeh_multipolygons,
        fill_color="orange",
        legend="MultiPolygons"
    )

    assert my_map.figure.plot_height == height
    assert my_map.figure.plot_width == width
    assert len(my_map.figure.renderers) == 2
    assert len(my_map.figure.tools) == 6
    # TODO improve !
