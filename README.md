# easy_map_bokeh
An easy way to map your geographic data (from a GeoDataFrame) with [bokeh >=__2.0.1__](https://github.com/bokeh/bokeh/tree/2.0.1)
Because it's boring to convert shapely geometry to bokeh format !!

![CI](https://github.com/amauryval/easy_map_bokeh/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/amauryval/easy_map_bokeh/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/easy_map_bokeh)

[![Anaconda-Server Badge](https://anaconda.org/amauryval/easy_map_bokeh/badges/version.svg)](https://anaconda.org/amauryval/easy_map_bokeh)
[![Anaconda-Server Badge](https://anaconda.org/amauryval/easy_map_bokeh/badges/latest_release_date.svg)](https://anaconda.org/amauryval/easy_map_bokeh)

[![Anaconda-Server Badge](https://anaconda.org/amauryval/easy_map_bokeh/badges/platforms.svg)](https://anaconda.org/amauryval/easy_map_bokeh)

[![Anaconda-Server Badge](https://anaconda.org/amauryval/easy_map_bokeh/badges/installer/conda.svg)](https://conda.anaconda.org/amauryval)


## How to install the conda package ?
Install Anaconda

then on your terminal:
```
conda install -c amauryval geo_bokeh
```


## How to use it ?!

A small example :
```python
from bokeh.plotting import show
import geopandas as gpd
from easy_map_bokeh import EasyMapBokeh

layers_to_add = [
    {
        "input_gdf": gpd.GeoDataFrame.from_file("your_geo_layer.geojson"),
        "legend": "My beautiful layer",
        "fill_color": "orange",  # optional
    }
]
# Points, LineString, MultiLineString, Polygons (+ holes) and MultiPolygons (+ holes) are supported

my_map = EasyMapBokeh(
    "My beautiful map",  # required: map title
    width=800,  # optional: figure width, default 800
    height=600,  # optional: figure width, default 600
    x_range=None,  # optional: x_range, default None
    y_range=None,  # optional: y_range, default None
    background_map_name="CARTODBPOSITRON",  # optional: background map name, default: CARTODBPOSITRON
    layers=layers_to_add    # optional: bokeh layer to add from a list of dict contains geodataframe settings, see dict above
)
# to get all the bokeh layer containers (dict), in order to update them (interactivity, slider... on a bokeh serve)
bokeh_layer_containers = my_map.get_bokeh_layer_containers

show(my_map.figure)
```

Check the jupyter notebook to find a more detailed example: 
```
jupyter notebook
```
And check 'example.ipynb'


Also, you can find a bokeh serve example with a slider widget.
On the terminal, run :
```
bokeh serve --show bokeh_serve_example.py
```
