"""
Module managing the canvas state and tool interactions.
"""

import py5


class CanvasManager:
    """
    Manages the drawing canvas, current tool, and the list of drawn shapes.

    This class handles user interactions with the canvas (e.g., placing shapes),
    rendering, and integrating with the undo/redo manager.
    """

    def __init__(self, hooks, undo_manager):
        """
        Initialize the CanvasManager.

        Args:
            hooks: A HookManager instance used to manage extension hooks.
            undo_manager: An UndoRedoManager instance to handle undo/redo operations.
        """
        self.hooks = hooks
        self.undo = undo_manager
        self.shapes = []
        self.current_tool = None

    def add_tool(self, tool):
        """
        Set the current active drawing tool.

        Args:
            tool: A drawing tool instance that supports the `place(x, y)` method.
        """
        self.current_tool = tool

    def handle_click(self, x, y):
        """
        Handle a click event on the canvas.

        Uses the current tool to create a shape at the given coordinates,
        appends the shape to the canvas, and records the action for undo/redo.

        Args:
            x (float): X-coordinate of the click.
            y (float): Y-coordinate of the click.
        """
        if self.current_tool:
            shape = self.current_tool.place(x, y)
            self.shapes.append(shape)
            self.undo.record(
                # pylint: disable-next=unnecessary-lambda
                lambda: self.shapes.pop(),
                # pylint: disable-next=unnecessary-lambda
                lambda: self.shapes.append(shape))

    def draw(self):
        """
        Render all shapes on the canvas.

        Iterates over the stored shapes and draws them using Py5.
        Supports 'rect' and 'ellipse' shape types.
        """
        for shape in self.shapes:
            py5.fill(0)
            py5.stroke(0)
            if shape['type'] == 'rect':
                py5.rect(shape['x'], shape['y'], shape['w'], shape['h'])
            elif shape['type'] == 'ellipse':
                py5.ellipse(shape['x'], shape['y'], shape['w'], shape['h'])
