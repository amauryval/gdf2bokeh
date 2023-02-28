import geopandas as gpd
import random
import pandas as pd
from shapely.geometry import Point
import numpy as np


class RandomPointsGenerator:
    __POINTS_CREATE = []

    def __init__(self, bounds, points_number) -> None:
        self._x_min, self._y_min, self._x_max, self._y_max = bounds
        self._points_number = points_number

        self.__build_points()

    def __build_points(self) -> None:
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
    def to_gdf(self) -> gpd.GeoDataFrame:
        df = pd.DataFrame(self.__POINTS_CREATE)
        geometry = df["geometry"]
        properties = df["id"]
        return gpd.GeoDataFrame(
            properties,
            geometry=geometry,
            crs='EPSG:3857'
        )


def build_data() -> gpd.GeoDataFrame:
    bounds = (-604158.2716, 5312679.2139, 1081125.3281, 6633511.0627)
    random_points = RandomPointsGenerator(bounds, 50).to_gdf
    random_points["value"] = np.random.randint(1, 6, random_points.shape[0])
    return random_points
