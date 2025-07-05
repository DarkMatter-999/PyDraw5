"""
Module managing the sidebar state and tool interactions.
"""

import py5


class Sidebar:
    """
    Represents the sidebar UI component containing tool buttons.

    Handles drawing the sidebar, managing tool buttons, and mouse interactions
    for selecting tools.
    """

    def __init__(self, hooks, canvas):
        """
        Initialize the Sidebar.

        Args:
            hooks: HookManager instance for extensibility (currently unused).
            canvas: CanvasManager instance to interact with the current tool.
        """
        self.hooks = hooks
        self.canvas = canvas
        self.tools = []
        self.tool_buttons = []
        self.icon_size = 32
        self.button_padding = 10
        self.sidebar_width = 150

    def add_tool_button(self, tool, icon_path):
        """
        Add a tool button to the sidebar with an icon loaded from the given path.

        Args:
            tool: The tool instance to associate with this button.
            icon_path (str): File path to the icon image.
        """
        img = py5.load_image(icon_path)
        self.tool_buttons.append({
            'tool': tool,
            'icon': img,
            'x': 10,
            'y': 10 + len(self.tool_buttons) * (self.icon_size + self.button_padding)
        })

    def draw(self):
        """
        Draw the sidebar background and all tool buttons.

        Highlights the currently selected tool with a border.
        """
        py5.fill(240)
        py5.rect(0, 0, self.sidebar_width, py5.height)

        for btn in self.tool_buttons:
            py5.image(
                btn['icon'],
                btn['x'],
                btn['y'],
                self.icon_size,
                self.icon_size)
            if self.canvas.current_tool == btn['tool']:
                py5.no_fill()
                py5.stroke(0)
                py5.rect(
                    btn['x'] - 2,
                    btn['y'] - 2,
                    self.icon_size + 4,
                    self.icon_size + 4)
                py5.no_stroke()

    def handle_mouse(self, x, y):
        """
        Handle mouse click events in the sidebar area.

        Selects a tool if a button is clicked.

        Args:
            x (int): X-coordinate of the mouse click.
            y (int): Y-coordinate of the mouse click.

        Returns:
            bool: True if the click was within the sidebar and handled,
                  False otherwise.
        """
        if x >= self.sidebar_width:
            return False

        for btn in self.tool_buttons:
            bx, by = btn['x'], btn['y']
            if bx <= x <= bx + self.icon_size and by <= y <= by + self.icon_size:
                self.canvas.current_tool = btn['tool']
                return True

        return True
