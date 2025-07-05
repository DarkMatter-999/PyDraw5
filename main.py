"""
Main sketch file for the drawing application.

Initializes the Py5 sketch, sets up tools, sidebar, canvas, and plugin loading.
"""

import os
import importlib.util

import py5

from hooks.hook_manager import HookManager
from canvas.canvas_manager import CanvasManager
from ui.sidebar import Sidebar
from state.undo_redo import UndoRedoManager
from tools.rectangle_tool import RectangleTool
from tools.ellipse_tool import EllipseTool

hook_manager = HookManager()
undo_manager = UndoRedoManager()
canvas_manager = CanvasManager(hook_manager, undo_manager)
sidebar = Sidebar(hook_manager, canvas_manager)


def setup():
    """Set up the Py5 sketch window, tools, and sidebar.

    Initializes canvas size, loads plugins, and adds drawing tools to the canvas and sidebar.
    """
    py5.size(2000, 1000)
    py5.background(255)
    load_plugins()

    rect_tool = RectangleTool(hook_manager)
    ellipse_tool = EllipseTool(hook_manager)

    canvas_manager.add_tool(rect_tool)

    sidebar.add_tool_button(rect_tool, "assets/icons/rectangle.png")
    sidebar.add_tool_button(ellipse_tool, "assets/icons/ellipse.png")


def draw():
    """Main draw loop for the Py5 sketch.

    Clears the background, then draws the canvas content and the UI sidebar.
    """
    py5.background(255)
    canvas_manager.draw()
    sidebar.draw()


def mouse_pressed():
    """Handle mouse press events.

    Delegates mouse input to the sidebar or canvas manager depending on click location.
    """
    if not sidebar.handle_mouse(py5.mouse_x, py5.mouse_y):
        canvas_manager.handle_click(py5.mouse_x, py5.mouse_y)


def key_pressed():
    """Handle key press events.

    Supports 'z' for undo and 'y' for redo actions through the UndoRedoManager.
    """
    if py5.key == 'z':
        undo_manager.undo()
    elif py5.key == 'y':
        undo_manager.redo()


def load_plugins():
    """Dynamically load and register plugins from the 'plugins' directory.

    Each plugin must define a `register` function that takes the hook manager as a parameter.
    """
    plugins_path = 'plugins'
    for filename in os.listdir(plugins_path):
        if filename.endswith('.py'):
            path = os.path.join(plugins_path, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            if spec:
                module = importlib.util.module_from_spec(spec)
                if spec.loader:
                    spec.loader.exec_module(module)
                    if hasattr(module, 'register'):
                        module.register(hook_manager)


py5.run_sketch()
