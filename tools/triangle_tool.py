"""
Module for the Triangle Tool.
"""

# pylint: disable-next=import-error
from tools.base_tool import BaseTool


class TriangleTool(BaseTool):
    """
    A drawing tool for placing triangle shapes on the canvas.

    This tool requires three clicks to define the three vertices of a triangle.
    It provides a preview of the triangle as points are being collected.
    """

    def __init__(self, hooks):
        """
        Initialize the TriangleTool.

        Args:
            hooks: A HookManager instance used to allow shape modification via hooks.
        """
        self.hooks = hooks
        self.name = "Triangle"
        self.vertices = []
        self.preview = None

    def handle_click(self, x, y):
        """
        Handle a click event on the canvas to define triangle vertices.

        Collects up to three clicks. On the third click, it forms a triangle
        shape, runs it through the 'shape.place' hook, and returns the shape
        to be placed on the canvas. Resets vertices after placing a shape.

        Args:
            x (float): X-coordinate of the mouse click.
            y (float): Y-coordinate of the mouse click.

        Returns:
            dict or None: A dictionary representing the triangle shape if three
                          vertices have been collected, otherwise None.
        """
        self.vertices.append((x, y))

        if len(self.vertices) == 3:
            x1, y1 = self.vertices[0]
            x2, y2 = self.vertices[1]
            x3, y3 = self.vertices[2]

            shape = {'type': 'triangle', 'x1': x1, 'y1': y1,
                     'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3}

            shape = self.hooks.run_hooks('shape.place', shape)
            self.vertices = []
            self.preview = None
            return shape

        return None

    def update_preview(self, x, y):
        """
        Update the preview of the triangle as vertices are being collected.

        If one vertex is collected, shows a line from the first vertex to the
        current mouse position. If two vertices are collected, shows a triangle
        from the first two vertices to the current mouse position.

        Args:
            x (float): Current X-coordinate of the mouse.
            y (float): Current Y-coordinate of the mouse.
        """
        if len(self.vertices) == 1:
            x1, y1 = self.vertices[0]
            self.preview = {'type': 'triangle', 'x1': x1, 'y1': y1,
                            'x2': x, 'y2': y, 'x3': x, 'y3': y}
        elif len(self.vertices) == 2:
            x1, y1 = self.vertices[0]
            x2, y2 = self.vertices[1]
            self.preview = {'type': 'triangle', 'x1': x1, 'y1': y1,
                            'x2': x2, 'y2': y2, 'x3': x, 'y3': y}

    def make_preview(self, x1, y1, x2, y2) -> dict:
        """
        This method is required by the BaseTool interface but is not used
        by the TriangleTool, as its preview logic is handled by `update_preview`.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Current X-coordinate of the drag.
            y2 (float): Current Y-coordinate of the drag.

        Returns:
            dict: The current preview shape, or None if no preview is active.
        """
        return self.preview

    def place(self, x1, y1, x2, y2) -> dict:
        """
        This method is required by the BaseTool interface but is not used
        by the TriangleTool, as its placement logic is handled by `handle_click`.

        Args:
            x1 (float): Starting X-coordinate of the drag.
            y1 (float): Starting Y-coordinate of the drag.
            x2 (float): Ending X-coordinate of the drag.
            y2 (float): Ending Y-coordinate of the drag.

        Returns:
            None: As placement is handled by `handle_click`.
        """
        return None


def register(hooks):
    """
    Registers the TriangleTool with the hook manager.

    Args:
        hooks: The HookManager instance to register the tool with.
    """
    tool = TriangleTool(hooks)
    hooks.run_hooks('tool.register', None, tool=tool,
                    icon_path='assets/icons/triangle.png')
