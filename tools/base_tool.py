"""
Module for defining base class for tools.
"""


class BaseTool:
    """
    Abstract base class for drawing tools.

    Subclasses should implement the `draw_preview` and `place` methods
    to define how the tool behaves visually and functionally.
    """

    def draw_preview(self, x, y):
        """
        Draw a preview of the shape at the given coordinates.

        This method is intended to be overridden by subclasses.

        Args:
            x (float): X-coordinate for the preview.
            y (float): Y-coordinate for the preview.
        """
        # pylint: disable-next=unnecessary-pass
        pass

    def place(self, x, y):
        """
        Place the shape at the given coordinates and return shape data.

        This method should return a dictionary representing the shape,
        including keys such as 'type', 'x', 'y', 'w', and 'h'.

        This method is intended to be overridden by subclasses.

        Args:
            x (float): X-coordinate where the shape should be placed.
            y (float): Y-coordinate where the shape should be placed.

        Returns:
            dict: A dictionary representing the placed shape.
        """
        # pylint: disable-next=unnecessary-pass
        pass
