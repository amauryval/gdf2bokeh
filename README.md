# gdf2bokeh
An easy way to map your geographic data (from a GeoDataFrame, a DataFrame and a list of dictionaries containing wkt or shapely geometries).

Yeah! Because it's boring to convert shapely geometry to bokeh format each time I need to map something !!

![CI](https://github.com/amauryval/gdf2bokeh/workflows/RunTest/badge.svg)
[![codecov](https://codecov.io/gh/amauryval/gdf2bokeh/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/gdf2bokeh)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/version.svg)](https://anaconda.org/amauryval/gdf2bokeh)
[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/latest_release_date.svg)](https://anaconda.org/amauryval/gdf2bokeh)
[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/platforms.svg)](https://anaconda.org/amauryval/gdf2bokeh)

[![PyPI version](https://badge.fury.io/py/gdf2bokeh.svg)](https://badge.fury.io/py/gdf2bokeh)


## How to install it ?

### with pip

```bash
pip install gdf2bokeh
```

### With Anaconda

```bash
conda install -c amauryval gdf2bokeh
```




## How to use it ?

A small example :

Check bokeh documentation in order to style your data :
    
* [bokeh marker style options](https://docs.bokeh.org/en/latest/docs/reference/models/markers.html) to style point features
* [bokeh multi_line style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_line) to style LineString and MultiLineString features
* [bokeh multi_polygon style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_polygons) to style polygon and multipolygons features

```python
from bokeh.plotting import show
import geopandas as gpd
from gdf2bokeh import Gdf2Bokeh

map_session = Gdf2Bokeh()

# add your layer from your data
map_session.add_layer_from_geodataframe("your_layer1", gpd.GeoDataFrame.from_file("your_geo_layer.geojson"))
map_session.add_layer_from_dataframe("your_layer2", gpd.GeoDataFrame.from_file("your_data.json"), 
                                     geom_column="geometry", geom_format="shapely")
map_session.add_layer_from_list_dict("your_layer3", gpd.GeoDataFrame.from_file("your_data.json"), 
                                     geom_column="geometry", geom_format="wkt")

# Let's go to register them on bokeh
map_session.add_layers_on_maps()

# Next, the map is displayed
show(map_session.figure)
```


Also, you can find a bokeh serve example with a slider widget.
On the terminal, run :

```bash
bokeh serve --show bokeh_serve_example.py
```
