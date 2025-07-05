"""
Module for defining base class for tools.
"""


class BaseTool:
    """
    Abstract base class for drawing tools.

    Subclasses should implement the `draw_preview` and `place` methods
    to define how the tool behaves visually and functionally.
    """

    def make_preview(self, x1, y1, x2, y2) -> dict:
        """
        Create a preview shape dictionary based on the given drag coordinates.

        This method is intended to be overridden by subclasses. It should return
        a dictionary representing the preview shape, similar to the `place` method.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Current X-coordinate of the drag.
            y2 (float): Current Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the preview shape.
        """
        raise NotImplementedError

    def place(self, x1, y1, x2, y2) -> dict:
        """
        Place the shape at the given coordinates and return shape data.

        This method should return a dictionary representing the placed shape,
        including keys such as 'type', 'x', 'y', 'w', and 'h' for rectangular
        or elliptical shapes, or 'x1', 'y1', 'x2', 'y2' for line shapes.

        This method is intended to be overridden by subclasses.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Ending X-coordinate of the drag.
            y2 (float): Ending Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the placed shape.
        """
        raise NotImplementedError
