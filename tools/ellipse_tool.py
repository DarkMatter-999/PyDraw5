"""
Module for Ellipse Tool.
"""

# pylint: disable-next=import-error
from tools.base_tool import BaseTool


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

    def make_preview(self, x1, y1, x2, y2):
        """
        Create a preview shape dictionary based on the given drag coordinates.

        This method should return a dictionary representing the preview shape.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Current X-coordinate of the drag.
            y2 (float): Current Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the preview shape.
        """
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        x = min(x1, x2)
        y = min(y1, y2)
        return {
            'type': 'ellipse',
            'x': x + w / 2,
            'y': y + h / 2,
            'w': w,
            'h': h}

    def place(self, x1, y1, x2, y2):
        """
        Create and return an ellipse shape at the specified location.

        The shape is passed through the 'shape.place' hook before being returned.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Ending X-coordinate of the drag.
            y2 (float): Ending Y-coordinate of the drag.

        Returns:
            dict: A dictionary representing the ellipse shape, 'type', 'x', 'y', 'w', and 'h'.
        """
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        x = min(x1, x2)
        y = min(y1, y2)
        return {
            'type': 'ellipse',
            'x': x + w / 2,
            'y': y + h / 2,
            'w': w,
            'h': h}


def register(hooks):
    """
    Registers the EllipseTool with the hook manager.

    Args:
        hooks: The HookManager instance to register the tool with.
    """
    tool = EllipseTool(hooks)
    hooks.run_hooks('tool.register', None, tool=tool,
                    icon_path='assets/icons/ellipse.png')
