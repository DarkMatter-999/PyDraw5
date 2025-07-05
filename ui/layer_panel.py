"""
Module for the LayerPanel class, which manages and displays layers in the UI.
"""

import py5


class LayerPanel:
    """
    Manages the display and interaction of layers in the user interface.

    Allows users to switch active layers, toggle visibility, and delete layers.
    """
    def __init__(self, canvas_manager):
        """
        Initializes the LayerPanel.

        Args:
            canvas_manager: The CanvasManager instance to interact with layers.
        """
        self.canvas = canvas_manager
        self.panel_width = 200
        self.entry_height = 40
        self.x = py5.width - self.panel_width
        self.hover_index = -1

    def draw(self):
        """
        Draws the layer panel, including layer entries and controls.
        """
        self.x = py5.width - self.panel_width
        py5.fill(240)
        py5.no_stroke()
        py5.rect(self.x, 0, self.panel_width, py5.height)

        for i, layer in enumerate(reversed(self.canvas.layers)):
            index = len(self.canvas.layers) - 1 - i
            y = i * self.entry_height
            is_active = index == self.canvas.current_layer_index
            is_hovered = index == self.hover_index

            if is_active:
                py5.fill(200, 220, 255)
            elif is_hovered:
                py5.fill(220)
            else:
                py5.fill(255)

            py5.stroke(180)
            py5.rect(self.x, y, self.panel_width, self.entry_height)

            py5.fill(0)
            py5.text_size(14)
            py5.text_align(py5.LEFT, py5.CENTER)
            py5.text(layer.name, self.x + 10, y + self.entry_height / 2)

            eye = 'O' if layer.visible else 'X'
            py5.text_align(py5.RIGHT, py5.CENTER)
            py5.text(
                eye,
                self.x +
                self.panel_width -
                10,
                y +
                self.entry_height /
                2)

            trash_icon_x = self.x + self.panel_width - 50
            py5.text_align(py5.LEFT, py5.CENTER)
            py5.text('🗑', trash_icon_x, y + self.entry_height / 2)

        py5.fill(0)
        py5.text_align(py5.CENTER, py5.BOTTOM)
        py5.text('+ Add Layer', self.x + self.panel_width / 2, py5.height - 10)

    def handle_mouse(self, mx, my):
        """
        Handles mouse click events on the layer panel.

        Args:
            mx (float): X-coordinate of the mouse click.
            my (float): Y-coordinate of the mouse click.

        Returns:
            bool: True if the click was handled by the layer panel, False otherwise.
        """
        if mx < self.x:
            return False

        num_layers = len(self.canvas.layers)
        if my > (num_layers * self.entry_height):
            self.canvas.add_layer()
            return True

        index = num_layers - 1 - int(my // self.entry_height)
        if 0 <= index < num_layers:

            trash_icon_x = self.x + self.panel_width - 50
            eye_icon_x = self.x + self.panel_width - 30

            if trash_icon_x <= mx < eye_icon_x:
                self.canvas.delete_layer(index)
            elif mx >= eye_icon_x:
                self.canvas.toggle_visibility(index)
            else:
                self.canvas.switch_layer(index)

            return True
        return False

    def handle_mouse_moved(self, mx, my):
        """
        Handles mouse movement events for hover effects on layer entries.

        Args:
            mx (float): X-coordinate of the mouse.
            my (float): Y-coordinate of the mouse.
        """
        if mx < self.x:
            self.hover_index = -1
            return

        index = len(self.canvas.layers) - 1 - int(my // self.entry_height)
        if 0 <= index < len(self.canvas.layers):
            self.hover_index = index
        else:
            self.hover_index = -1
