# Gdf2Bokeh
An easy way to map your geographic data (from a GeoDataFrame, a DataFrame and a list of dictionaries containing wkt or shapely geometries).

Yeah! Because it's boring to convert shapely geometry to bokeh format each time I need to map something !!

Also, this library let you to build complex Bokeh dashboard: no limitations to use Bokeh mecanisms.

[![CI](https://github.com/amauryval/gdf2bokeh/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/amauryval/gdf2bokeh/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/amauryval/gdf2bokeh/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/gdf2bokeh)

[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/version.svg)](https://anaconda.org/amauryval/gdf2bokeh)
[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/latest_release_date.svg)](https://anaconda.org/amauryval/gdf2bokeh)
[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/platforms.svg)](https://anaconda.org/amauryval/gdf2bokeh)

[![PyPI version](https://badge.fury.io/py/gdf2bokeh.svg)](https://badge.fury.io/py/gdf2bokeh)

Check the demo [here](https://amauryval.github.io/gdf2bokeh/)


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

Gdf2Bokeh is able to map your data from various format. About data, you must be aware to use compliant geometry types:

It supports Geo/DataFrame/List of dict/List of geometry containing these 4 geometries families:

* Point data with Point geometry
* MultiPoint data with MultiPoint geometry
* Line data with LineString and/or MultiLineString geometries
* Polygon data with Polygon and/or MultiPolygon geometries

GeometryCollection data are not supported, so explode it to use it. So the best practice consists to split your input 
data by geometry type. 

And you'll be able, optionally, to style your data thanks to the bokeh arguments :
Check bokeh documentation in order to style your data :
    
* Point / MultiPoint families: [bokeh marker style options](https://docs.bokeh.org/en/latest/docs/reference/models/markers.html)
* Line family: [bokeh multi_line style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_line)
* Polygon family: [bokeh multi_polygon style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_polygons)


### A simple example

```python
from bokeh.plotting import show
import geopandas as gpd
import paandas as pd
from gdf2bokeh import Gdf2Bokeh

map_session = Gdf2Bokeh()

# add your layer from your data

# Map a points GeoDataFrame. You can see marker style arguments, so we suppose that input_data contains Point geometry
map_session.add_layer_from_geodataframe("layer1", gpd.GeoDataFrame.from_file("your_poins_data.geojson"),
                                        size=6, fill_color="red", line_color="blue")

# Map from a DataFrame. Style parameters are not required
map_session.add_layer_from_dataframe("layer2", pd.DataFrame.from_file("your_data.json"),
                                     geom_column="geometry", geom_format="shapely")

# Map from a list of dictionnaries
map_session.add_layer_from_dict_list("layer3", 
                                     [
                                         {"geometry": "POINT(0 0)", "col1": "value1"},
                                         {"geometry": "POINT(1 1)", "col1": "value2"}
                                     ],
                                     geom_column="geometry", geom_format="wkt")

# Map from a geometry (shapely, wkt...) list
map_session.add_layer_from_geom_list("layer4", ["Point(0 0)", "Point(5 5)"], geom_format="wkt")

# Let's go to register them on bokeh
map_session.add_layers_on_map()

# Next, the map is displayed
show(map_session.figure)
```


Here a bokeh basic example.
On the terminal, run :

```bash
python examples/bokeh_simple_case_example.py
```

Or you can use the jupyter notebook 'example.ipynb'

### An advanced example

Here a bokeh serve example with a slider widget.
On the terminal, run :

```bash
bokeh serve --show examples/bokeh_serve_example.py
```
