from bokeh.plotting import figure


class AppMap:

    def __init__(
        self,
        title: str = "My empty Map",
        width: int = 800,
        height: int = 600,
        background_map_name: str = "CARTODBPOSITRON",
    ) -> None:
        """
        :param title: figure title
        :type title: str
        :param width: width value
        :type width: int
        :param height: height value
        :type height: int
        :param background_map_name: background map name
        :type background_map_name: str
        """
        super().__init__()

        self.figure = figure(
            title=title,
            output_backend="webgl",
            tools=["pan", "wheel_zoom", "box_zoom", "reset", "save"],
        )

        self.figure.width = width
        self.figure.height = height

        self._add_background_map(background_map_name)

    def _legend_settings(self) -> None:
        # interactive legend
        self.figure.legend.click_policy = "hide"

    def _add_background_map(self, background_map_name: str) -> None:
        self.figure.add_tile(background_map_name)
