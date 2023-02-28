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

Gdf2Bokeh is able to map your data from various format. About data, you must be aware to use compliant geometry types:

It supports data containing these geometries families:

* Point family: Point
* Line family: LineString and/or MultiLineString
* Polygon family: Polygon and/or MultiPolygon

GeometryCollection data are not supported, so explode it to use it. So the best practice consists to split your input 
data by geometry type. 

And you'll be able, optionally, to style your data thanks to the bokeh arguments :
Check bokeh documentation in order to style your data :
    
* Point family: [bokeh marker style options](https://docs.bokeh.org/en/latest/docs/reference/models/markers.html)
* Line family: [bokeh multi_line style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_line)
* Polygon family: [bokeh multi_polygon style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_polygons)


A small example :

```python
from bokeh.plotting import show
import geopandas as gpd
from gdf2bokeh import Gdf2Bokeh

map_session = Gdf2Bokeh()

# add your layer from your data

# Map a points GeoDataFrame. You can see marker style arguments, so we suppose that input_data contains Point geometry
map_session.add_layer_from_geodataframe("layer1", gpd.GeoDataFrame.from_file("your_poins_data.geojson"), 
                                        size=6, fill_color="red", line_color="blue")  

# Map from a DataFrame. Style parameters are not required
map_session.add_layer_from_dataframe("layer2", gpd.GeoDataFrame.from_file("your_data.json"),
                                     geom_column="geometry", geom_format="shapely")

# Map from a list of dictionnaries
map_session.add_layer_from_dict_list("layer3", gpd.GeoDataFrame.from_file("your_data.json"),
                                     geom_column="geometry", geom_format="wkt")

# Map from a geometry (shapely, wkt...) list
map_session.add_layer_from_geom_list("layer4", ["Point(0 0)", "Point(5 5)"], geom_format="wkt")


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
