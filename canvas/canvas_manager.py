"""
Module managing the canvas state and tool interactions.
"""

import py5

# pylint: disable-next=too-many-instance-attributes
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

        self.placing = False
        self.start_x = 0
        self.start_y = 0
        self.preview_shape = None

    def add_tool(self, tool):
        """
        Set the current active drawing tool.

        Args:
            tool: A drawing tool instance that supports the `place(x, y)` method.
        """
        self.current_tool = tool

    def start_place(self, x, y):
        """
        Handle a click event on the canvas.

        Uses the current tool to create a shape at the given coordinates,
        appends the shape to the canvas, and records the action for undo/redo.

        Args:
            x (float): X-coordinate of the click.
            y (float): Y-coordinate of the click.
        """
        self.placing = True
        self.start_x = x
        self.start_y = y
        self.preview_shape = None

    def update_preview(self, x, y):
        """
        Update the preview on the canvas.

        Uses the current tool to create a shape preview based on the drag,
        while dragging.

        Args:
            x (float): Current X-coordinate of the mouse during the drag.
            y (float): Current Y-coordinate of the mouse during the drag.
        """
        if self.current_tool and self.placing:
            self.preview_shape = self.current_tool.make_preview(self.start_x, self.start_y, x, y)


    def finish_place(self, x, y):
        """
        Handle a release event on the canvas.

        Uses the current tool to place a shape based on the drag,
        and appends the final shape to the canvas when the mouse is released.

        Args:
            x (float): X-coordinate where the mouse was released.
            y (float): Y-coordinate where the mouse was released.
        """
        if self.current_tool and self.placing:
            shape = self.current_tool.place(self.start_x, self.start_y, x, y)
            shape = self.hooks.run_hooks('shape.place', shape)
            self.shapes.append(shape)
            # pylint: disable-next=unnecessary-lambda
            self.undo.record(lambda: self.shapes.pop(), lambda: self.shapes.append(shape))

        self.placing = False
        self.preview_shape = None

    def draw(self):
        """
        Render all shapes on the canvas.

        Iterates over the stored shapes and draws them.
        """
        for shape in self.shapes:
            self.draw_shape(shape)

        if self.preview_shape:
            self.draw_shape(self.preview_shape, preview=True)

    def draw_shape(self, shape, preview=False):
        """
        Draw the shape on the canvas.

        Supports 'rect' and 'ellipse' shape types.
        Args:
            shape (BaseTool): Shape instance.
            preview (bool): Whether the shape is a preview.
        """
        handled = self.hooks.run_hooks('shape.draw', False, shape=shape, preview=preview)

        if handled:
            return

        py5.stroke(0, 100 if preview else 255)
        py5.no_fill()

        if shape['type'] == 'rect':
            py5.rect(shape['x'], shape['y'], shape['w'], shape['h'])
        elif shape['type'] == 'ellipse':
            py5.ellipse(shape['x'], shape['y'], shape['w'], shape['h'])
        elif shape['type'] == 'line':
            py5.line(shape['x1'], shape['y1'], shape['x2'], shape['y2'])

        py5.no_stroke()
