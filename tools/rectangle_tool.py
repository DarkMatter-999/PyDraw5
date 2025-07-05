"""
Module for rectangle tool.
"""

import py5
from base_tool import BaseTool

class RectangleTool(BaseTool):
    """
    A drawing tool for placing rectangle shapes on the canvas.

    Uses a fixed size for the rectangle and allows hooks to modify the shape data.
    """

    def __init__(self, hooks):
        """
        Initialize the RectangleTool.

        Args:
            hooks: A HookManager instance used to allow shape modification via hooks.
        """
        self.hooks = hooks
        self.name = "Rectangle"

    def draw_preview(self, x, y):
        """
        Draw a preview of the rectangle at the specified location.

        Args:
            x (float): X-coordinate for the preview.
            y (float): Y-coordinate for the preview.
        """
        py5.rect(x, y, 100, 100)

    def place(self, x, y):
        """
        Create and return a rectangle shape at the specified location.

        The shape is passed through the 'shape.place' hook before being returned.

        Args:
            x (float): X-coordinate of the rectangle.
            y (float): Y-coordinate of the rectangle.

        Returns:
            dict: A dictionary representing the rectangle shape, 'type', 'x', 'y', 'w', and 'h'.
        """
        shape = {'type': 'rect', 'x': x, 'y': y, 'w': 100, 'h': 100}
        shape = self.hooks.run_hooks('shape.place', shape)
        return shape
