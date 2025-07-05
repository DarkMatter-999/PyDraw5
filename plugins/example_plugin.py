"""
Plugin that tweaks rectangle shapes by randomly modifying their position and size.

Registers a hook to adjust rectangles during placement using the 'shape.place' hook.
"""

def tweak_rect(shape):
    """
    Randomly modify the position and size of a rectangle shape.

    Args:
        shape (dict): The shape dictionary to potentially modify.
        *args: Additional positional arguments (ignored).
        **kwargs: Additional keyword arguments (ignored).

    Returns:
        dict: The modified shape (only if it's a rectangle).
    """
    # if shape['type'] == 'rect' or shape['type'] == 'ellipse':
    #     shape['x'] += random.randint(-5, 5)
    #     shape['y'] += random.randint(-5, 5)
    #     shape['w'] += random.randint(-50, 50)
    #     shape['h'] += random.randint(-50, 50)
    return shape


def register(hooks):
    """
    Register the tweak_rect function to the 'shape.place' hook.

    Args:
        hooks: An instance of HookManager.
    """
    hooks.add_hook('shape.place', tweak_rect)
