"""
Module managing the undo/redo states from tool interactions.
"""


class UndoRedoManager:
    """
    Manages undo and redo operations by storing actions as callable pairs.

    Each recorded action consists of an undo function and a redo function,
    enabling users to revert or reapply changes in order.
    """

    def __init__(self):
        """
        Initialize the UndoRedoManager with empty undo and redo stacks.
        """
        self.undo_stack = []
        self.redo_stack = []

    def record(self, undo_func, redo_func):
        """
        Record a new action to the undo stack.

        Args:
            undo_func (callable): Function to revert the action.
            redo_func (callable): Function to reapply the action.

        Side Effects:
            Clears the redo stack, as new actions invalidate redo history.
        """
        self.undo_stack.append((undo_func, redo_func))
        self.redo_stack.clear()

    def undo(self):
        """
        Perform the most recent undoable action.

        Calls the stored undo function and pushes the action onto the redo stack.
        """
        if self.undo_stack:
            undo, redo = self.undo_stack.pop()
            undo()
            self.redo_stack.append((undo, redo))

    def redo(self):
        """
        Reapply the most recently undone action.

        Calls the stored redo function and pushes the action back onto the undo stack.
        """
        if self.redo_stack:
            undo, redo = self.redo_stack.pop()
            redo()
            self.undo_stack.append((undo, redo))
