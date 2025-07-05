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

hook_manager = HookManager()
undo_manager = UndoRedoManager()
canvas_manager = CanvasManager(hook_manager, undo_manager)
sidebar = Sidebar(hook_manager, canvas_manager)
tool_registry = []


def on_tool_register(value, tool, icon_path):
    """
    Callback function to register tools.

    This hook appends the tool and its icon path to the tool_registry list.

    Args:
        value: The original value passed to the hook (not used in this case).
        tool: The tool instance to be registered.
        icon_path: The path to the tool's icon.

    Returns:
        The original value (or None, as it's not used).
    """
    tool_registry.append((tool, icon_path))
    return value

hook_manager.add_hook('tool.register', on_tool_register)

def load_core_tools():
    """
    Loads core drawing tools by importing their modules and registering them.

    This function iterates through a predefined list of tool modules,
    imports each one, and calls its `register` function to integrate
    the tool with the application's hook manager.
    """
    tool_modules = ['tools.rectangle_tool', 'tools.ellipse_tool', 'tools.line_tool']
    for mod_name in tool_modules:
        module = importlib.import_module(mod_name)
        if hasattr(module, 'register'):
            module.register(hook_manager)

def setup():
    """Set up the Py5 sketch window, tools, and sidebar.

    Initializes canvas size, loads plugins, and adds drawing tools to the canvas and sidebar.
    """
    py5.size(2000, 1000)
    py5.background(255)
    load_plugins()

    load_core_tools()

    for tool, icon in tool_registry:
        sidebar.add_tool_button(tool, icon)

    if tool_registry:
        canvas_manager.add_tool(tool_registry[0][0])


def draw():
    """Main draw loop for the Py5 sketch.

    Clears the background, then draws the canvas content and the UI sidebar.
    """
    py5.background(255)
    canvas_manager.draw()
    sidebar.draw()


def mouse_pressed():
    """Handle mouse press events.

    Initiates shape placement or interaction with the sidebar.
    Records the starting coordinates for drag operations if a tool is active.
    """
    if not sidebar.handle_mouse(py5.mouse_x, py5.mouse_y):
        canvas_manager.start_place(py5.mouse_x, py5.mouse_y)

def mouse_dragged():
    """Handle mouse drag events.

    Continuously updates the preview of the shape being drawn on the canvas
    as the mouse is dragged.
    """
    canvas_manager.update_preview(py5.mouse_x, py5.mouse_y)

def mouse_released():
    """Handle mouse release events.

    Finalizes the placement of the shape on the canvas and records the action
    for undo/redo.
    """
    canvas_manager.finish_place(py5.mouse_x, py5.mouse_y)

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
