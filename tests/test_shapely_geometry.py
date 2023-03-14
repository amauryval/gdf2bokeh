from gdf2bokeh.geometry import geometry_2_bokeh_format


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
