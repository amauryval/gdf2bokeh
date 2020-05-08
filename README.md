# Bokeh_for_easy_map
An easy way to map your geographic data (from a GeoDataFrame) with bokeh


## How to install it ?

On your terminal:
```
conda env create -f environment.yml
activate bfm
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
from bokeh_for_map import BokehForMap

my_polygons = gpd.GeoDataFrame.from_file("my_input_data.geojson")

# Init bokeh session
my_map = BokehForMap("My beautiful map", width=640, height=800)

# now you can add layer on you bokeh figure
my_map.add_polygons(
    my_polygons,  # a geodataframe
    fill_color="red",
    legend="Polygons"
)

show(my_map.figure)
```

### BokehForMap python class contains these methods

__To add layers__
* .add_lines() : for LineString and MultiLineStrings
* .add_polygons() : for polygons and MultiPolygons (holes supported)
* .add_points() : for Points. MultiPoint are not supported

__To get bokeh figure object__:
* .figure : useful to play with all bokeh methods
