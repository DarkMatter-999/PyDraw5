"""
Module for rectangle tool.
"""

from tools.base_tool import BaseTool

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

    def make_preview(self, x1, y1, x2, y2):
        """
        Draw a preview of the rectangle at the specified location.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Current X-coordinate of the drag.
            y2 (float): Current Y-coordinate of the drag.
        """
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        x = min(x1, x2)
        y = min(y1, y2)
        return {'type': 'rect', 'x': x, 'y': y, 'w': w, 'h': h}


    def place(self, x1, y1, x2, y2):
        """
        Create and return a rectangle shape at the specified location.

        The shape is passed through the 'shape.place' hook before being returned.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Ending X-coordinate of the drag.
            y2 (float): Ending Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the rectangle shape, 'type', 'x', 'y', 'w', and 'h'.
        """
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        x = min(x1, x2)
        y = min(y1, y2)
        return {'type': 'rect', 'x': x, 'y': y, 'w': w, 'h': h}

def register(hooks):
    """
    Registers the RectangleTool with the hook manager.

    Args:
        hooks: The HookManager instance to register the tool with.
    """
    tool = RectangleTool(hooks)
    hooks.run_hooks('tool.register', None, tool=tool, icon_path='assets/icons/rectangle.png')
