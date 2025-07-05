"""
Module for Ellipse Tool.
"""

import py5
from base_tool import BaseTool

class EllipseTool(BaseTool):
    """
    A drawing tool for placing ellipse shapes on the canvas.

    Uses a fixed size for the ellipse and allows hooks to modify the shape data.
    """

    def __init__(self, hooks):
        """
        Initialize the EllipseTool.

        Args:
            hooks: A HookManager instance used to allow shape modification via hooks.
        """
        self.hooks = hooks
        self.name = "Ellipse"

    def draw_preview(self, x, y):
        """
        Draw a preview of the ellipse at the specified location.

        Args:
            x (float): X-coordinate for the preview.
            y (float): Y-coordinate for the preview.
        """
        py5.ellipse(x, y, 50, 50)

    def place(self, x, y):
        """
        Create and return an ellipse shape at the specified location.

        The shape is passed through the 'shape.place' hook before being returned.

        Args:
            x (float): X-coordinate of the ellipse.
            y (float): Y-coordinate of the ellipse.

        Returns:
            dict: A dictionary representing the ellipse shape, 'type', 'x', 'y', 'w', and 'h'.
        """
        shape = {'type': 'ellipse', 'x': x, 'y': y, 'w': 50, 'h': 50}
        shape = self.hooks.run_hooks('shape.place', shape)
        return shape
