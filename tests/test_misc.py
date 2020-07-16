from easy_map_bokeh.helpers.misc import color_based_on_the_string_value


def test_bokeh_session(width, height):
    a_color = color_based_on_the_string_value("My beautiful map")

    assert a_color == "#f751aa"
