"""
Module for the Line Tool.
"""

# pylint: disable-next=import-error
from tools.base_tool import BaseTool

class LineTool(BaseTool):
    """
    A drawing tool for placing line shapes on the canvas.

    This tool allows users to draw lines by defining a start and end point
    through dragging on the canvas.
    """
    def __init__(self, hooks):
        self.hooks = hooks
        self.name = "Line"

    def make_preview(self, x1, y1, x2, y2):
        """
        Create a preview shape dictionary based on the given coordinates and dimensions.

        This method should return a dictionary representing the preview shape.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Current X-coordinate of the drag.
            y2 (float): Current Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the preview shape.
        """
        return {'type': 'line', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

    def place(self, x1, y1, x2, y2):
        """
        Create and return a line shape at the specified location.

        The shape is passed through the 'shape.place' hook before being returned.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Ending X-coordinate of the drag.
            y2 (float): Ending Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the line shape, 'type', 'x1', 'y1', 'x2', and 'y2'.
        """
        return {'type': 'line', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def register(hooks):
    """
    Registers the LineTool with the hook manager.

    Args:
        hooks: The HookManager instance to register the tool with.
    """
    tool = LineTool(hooks)
    hooks.run_hooks('tool.register', None, tool=tool, icon_path='assets/icons/line.png')
