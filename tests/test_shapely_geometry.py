from gdf2bokeh.geometry import geometry_2_bokeh_format
from gdf2bokeh.geometry import check_multilinestring_continuity


def test_shapely_point_geom_to_bokeh_format(shapely_point):

    output = geometry_2_bokeh_format(shapely_point, "xy")
    assert output == (0.0, 1.0)

    output = geometry_2_bokeh_format(shapely_point, "x")
    assert output == 0.0

    output = geometry_2_bokeh_format(shapely_point, "y")
    assert output == 1.0


def test_shapely_linestring_geom_to_bokeh_format(shapely_linestring):

    output = geometry_2_bokeh_format(shapely_linestring, "xy")
    assert output == [(0.0, 0.0), (1.0, 2.0)]

    output = geometry_2_bokeh_format(shapely_linestring, "x")
    assert output == [0.0, 1.0]

    output = geometry_2_bokeh_format(shapely_linestring, "y")
    assert output == [0.0, 2.0]


def test_shapely_polygon_geom_to_bokeh_format(shapely_polygon):

    output = geometry_2_bokeh_format(shapely_polygon, "xy")
    assert output == [[[(0.0, 0.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)]]]

    output = geometry_2_bokeh_format(shapely_polygon, "x")
    assert output == [[[0.0, 1.0, 1.0, 0.0]]]

    output = geometry_2_bokeh_format(shapely_polygon, "y")
    assert output == [[[0.0, 1.0, 0.0, 0.0]]]


def test_shapely_polygon_with_hole_geom_to_bokeh_format(shapely_polygon_with_hole):

    output = geometry_2_bokeh_format(shapely_polygon_with_hole, "xy")
    assert output == [[
        [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]],
        [[(1.0, 2.0), (5.0, 2.0), (5.0, 1.0), (1.0, 1.0), (1.0, 2.0)],
         [(9.0, 9.0), (9.0, 8.0), (8.0, 8.0), (8.0, 9.0), (9.0, 9.0)]]
    ]

    output = geometry_2_bokeh_format(shapely_polygon_with_hole, "x")
    assert output == [[[0.0, 10.0, 10.0, 0.0, 0.0]], [[1.0, 5.0, 5.0, 1.0, 1.0], [9.0, 9.0, 8.0, 8.0, 9.0]]]

    output = geometry_2_bokeh_format(shapely_polygon_with_hole, "y")
    assert output == [[[0.0, 0.0, 10.0, 10.0, 0.0]], [[2.0, 2.0, 1.0, 1.0, 2.0], [9.0, 8.0, 8.0, 9.0, 9.0]]]


def test_shapely_multilinestring_geom_to_bokeh_format(shapely_multilinestring_without_continuity):

    output = geometry_2_bokeh_format(shapely_multilinestring_without_continuity, "xy")
    assert output == [(0.0, 0.0), (5.0, 2.0), (6.0, 0.0), (10.0, 10.0)]

    output = geometry_2_bokeh_format(shapely_multilinestring_without_continuity, "x")
    assert output == [0.0, 5.0, 6.0, 10.0]

    output = geometry_2_bokeh_format(shapely_multilinestring_without_continuity, "y")
    assert output == [0.0, 2.0, 0.0, 10.0]


def test_check_multilinestring_without_continuity(shapely_multilinestring_without_continuity):
    output = check_multilinestring_continuity(shapely_multilinestring_without_continuity)
    assert len(output) == 2
    assert set([feature.geom_type for feature in output]) == {"LineString"}


def test_check_multilinestring_continuity(shapely_multilinestring_continuity):
    output = check_multilinestring_continuity(shapely_multilinestring_continuity)
    assert len(output) == 1
    assert output[0].geom_type == "MultiLineString"


def test_check_multilinestring_unordered_to_reordered(shapely_multilinestring_unordered):
    output = check_multilinestring_continuity(shapely_multilinestring_unordered)
    assert len(output) == 1
    assert output[0].geom_type == "MultiLineString"
    assert output[0].wkt == "MULTILINESTRING ((0 0, 5 2), (5 2, 10 10))"

