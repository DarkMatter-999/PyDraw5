"""
Module to save the drawing in JSON format.
"""

import json


def save_shapes(shapes, filename='art.json'):
    """
    Save a list of shape dictionaries to a JSON file.

    Args:
        shapes (list): A list of shape dictionaries, each containing
                       properties like 'type', 'x', 'y', 'w', 'h'.
        filename (str): The name of the file to save to. Defaults to 'art.json'.

    Raises:
        IOError: If there is an issue writing to the file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(shapes, f, indent=2)
