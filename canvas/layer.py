"""
Module for the Layer class, representing a single layer in the drawing canvas.
"""

class Layer:
    """
    Represents a single layer within the drawing canvas.

    Each layer contains its own set of shapes,
    and has properties for visibility and lock status.
    """
    def __init__(self, name):
        """
        Initializes a new Layer instance.

        Args:
            name (str): The name of the layer.
        """
        self.name = name
        self.shapes = []
        self.visible = True
        self.locked = False
