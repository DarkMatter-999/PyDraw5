"""
Module managing the canvas state and tool interactions.
"""

import py5
from canvas.layer import Layer

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
        self.current_layer_index = 0
        self.layers = []

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
            self.preview_shape = self.current_tool.make_preview(
                self.start_x, self.start_y, x, y)

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

            layer = self.get_current_layer()
            if layer and not layer.locked:
                layer.shapes.append(shape)
                self.undo.record(
                    lambda: layer.shapes.pop(),
                    lambda: layer.shapes.append(shape)
                )

        self.placing = False
        self.preview_shape = None

    def draw(self):
        """
        Render all shapes on the canvas.

        Iterates over the stored shapes and draws them.
        """
        for layer in self.layers:
            if not layer.visible:
                continue
            for shape in layer.shapes:
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
        handled = self.hooks.run_hooks(
            'shape.draw', False, shape=shape, preview=preview)

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
        elif shape['type'] == 'triangle':
            py5.triangle(shape['x1'], shape['y1'],
                         shape['x2'], shape['y2'],
                         shape['x3'], shape['y3'])

        py5.no_stroke()

    def add_layer(self, name=None):
        """
        Adds a new layer to the canvas.

        If a name is not provided, a default name "Layer X" is generated.
        The new layer becomes the current active layer.

        Args:
            name (str, optional): The name of the new layer. Defaults to None.
        """
        name = name or f"Layer {len(self.layers) + 1}"
        self.layers.append(Layer(name))
        self.current_layer_index = len(self.layers) - 1

    def get_current_layer(self):
        """
        Returns the currently active layer.

        Returns:
            Layer or None: The current Layer object, or None if no layers exist.
        """
        return self.layers[self.current_layer_index] if self.layers else None

    def delete_layer(self, index):
        """
        Delete the layer at the given index.
        """
        if len(self.layers) <= 1:
            print("Can't delete the last layer.")
            return

        layer = self.layers[index]

        should_delete = self.hooks.run_hooks(
            'layer.delete', True, layer=layer, index=index)
        if not should_delete:
            return

        removed = self.layers.pop(index)
        self.current_layer_index = max(
            0, self.current_layer_index - (1 if index <= self.current_layer_index else 0))

        self.hooks.run_hooks('layer.deleted', None, layer=removed, index=index)

    def toggle_visibility(self, index):
        """
        Toggle the visibility of the layer at the given index.

        Args:
            index (int): The index of the layer to toggle visibility for.
        """
        if 0 <= index < len(self.layers):
            self.layers[index].visible = not self.layers[index].visible

    def toggle_lock(self, index):
        """
        Toggle the locked state of the layer at the given index.

        Args:
            index (int): The index of the layer to toggle lock for.
        """
        if 0 <= index < len(self.layers):
            self.layers[index].locked = not self.layers[index].locked

    def switch_layer(self, index):
        """
        Switches the current active layer to the specified index.

        Args:
            index (int): The index of the layer to switch to.
        """
        if 0 <= index < len(self.layers):
            self.current_layer_index = index

    def move_layer(self, from_index, to_index):
        """
        Moves a layer from one position to another within the layer stack.

        Args:
            from_index (int): The current index of the layer to move.
            to_index (int): The target index where the layer should be moved.
        """
        if 0 <= from_index < len(
                self.layers) and 0 <= to_index < len(
                self.layers):
            layer = self.layers.pop(from_index)
            self.layers.insert(to_index, layer)
            if self.current_layer_index == from_index:
                self.current_layer_index = to_index
