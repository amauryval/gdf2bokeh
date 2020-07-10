# Bokeh_for_easy_map
An easy way to map your geographic data (from a GeoDataFrame) with [bokeh __2.0.1__](https://github.com/bokeh/bokeh/tree/2.0.1)


![CI](https://github.com/wiralyki/Bokeh_for_easy_map/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/wiralyki/Bokeh_for_easy_map/branch/master/graph/badge.svg)](https://codecov.io/gh/wiralyki/Bokeh_for_easy_map)

![conda_pf](https://anaconda.org/amauryval/geo_bokeh/badges/platforms.svg)
![conda_installer](https://anaconda.org/amauryval/geo_bokeh/badges/installer/conda.svg)

## How to install the conda package ?
Install Anaconda

then on your terminal:
```
conda install -c amauryval geo_bokeh
```


## How to install the repository ?

On your terminal:
```
conda env create -f environment.yml
activate bokeh_for_map
```

## How to test it ?

Play with the jupyter notebook named "example.ipynb". Documentation is coming !

On your terminal:
```
jupyter notebook
```

## Example:

```python
from bokeh.plotting import show
import geopandas as gpd
from geo_bokeh import BokehForMap

# Init bokeh session
my_map = BokehForMap(
    title="My beautiful map",
    width=640,
    height=800,
    background_map_name="STAMEN_TONER"
)

# convert file data to geojson
my_polygons = gpd.GeoDataFrame.from_file("my_input_data.geojson")
# now you can format data with the "format_features" method contained in the BokehForMap class
bokeh_polygons = my_map.format_gdf_features_to_bokeh(my_polygons)

# now we can plot data
my_map.add_polygons(
    bokeh_polygons["data"],  # you can found "format" key if you want to play with widget
    fill_color="red",
    legend="Polygons"
)

show(my_map.figure)
```

You can find a bokeh serve example with a slider widget.
On the terminal, run :
```
bokeh serve --show bokeh_serve_example.py
```


### BokehForMap python class contains these methods

__to format geodataframe input data__
* .get_bokeh_structure_from_gdf_features(): to get the bokeh structure from geodataframe 
* .format_gdf_features_to_bokeh(): to format data from geodataframe to bokeh 

__To add layers__
* .add_lines(): for LineString and MultiLineStrings
* .add_polygons(): for polygons and MultiPolygons (holes supported)
* .add_points(): for Points. MultiPoint are not supported

__To get bokeh figure object__:
* .figure: useful to play with all bokeh methods

