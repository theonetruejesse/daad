# Helper class, use with @Singleton decorator to turn a class into a singleton
# https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
"""
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.
"""

class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated
        self._instance = None
        self._lock = False  # Prevent reinitialization

    def instance(self, *args, **kwargs):
        """
        Returns the singleton instance. Ensures the cache session is warmed up.
        """
        if self._instance is None:
            if self._lock:  # Avoid reinitializing if already called
                raise RuntimeError("Instance already exists; cannot reinitialize.")
            self._lock = True
            self._instance = self._decorated(*args, **kwargs)
        return self._instance

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            return self.instance(*args, **kwargs)
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
