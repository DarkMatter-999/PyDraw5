"""
Module managing the whole hooks system.
"""


class HookManager:
    """
    Manages hooks for extensibility by allowing registration and execution of callbacks.

    Hooks enable plugins or external modules to modify or react to events in the system.
    """

    def __init__(self):
        """
        Initialize the HookManager with an empty hook registry.
        """
        self._hooks = {}

    def add_hook(self, name, callback, priority=10):
        """
        Register a callback function to a named hook.

        Args:
            name (str): The name of the hook to register under.
            callback (callable): A function to be called when the hook is triggered.
                                 It should accept the value and any additional arguments.
            priority (int, optional): Determines execution order. Lower numbers run earlier.
                                      Defaults to 10.
        """
        self._hooks.setdefault(name, []).append((priority, callback))
        # pylint: disable-next=unnecessary-lambda
        self._hooks[name].sort(key=lambda x: x[0])

    # pylint: disable-next=keyword-arg-before-vararg
    def run_hooks(self, name, value=None, *args, **kwargs):
        """
        Execute all callbacks registered to the specified hook name.

        Each callback may modify and return a new value, which is passed to the next.
        If a callback returns None, the current value is preserved.

        Args:
            name (str): The name of the hook to execute.
            value (any, optional): The initial value passed to the callbacks. Defaults to None.
            *args: Additional positional arguments passed to each callback.
            **kwargs: Additional keyword arguments passed to each callback.

        Returns:
            any: The final modified value after all callbacks have been run.
        """
        for _, callback in self._hooks.get(name, []):
            result = callback(value, *args, **kwargs)
            if result is not None:
                value = result
        return value
