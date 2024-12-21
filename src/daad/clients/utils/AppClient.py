from abc import abstractmethod


class AppClient:
    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def _setup(self):
        pass

    """
        AppClient is a singleton class that ensures the client is initialized only once.
        https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
    """

    def __init__(self, decorated):
        self.client = None
        self._setup()
        # singleton pattern
        self._decorated = decorated
        self._instance = None
        self._lock = False  # Prevent reinitialization

    def instance(self, *args, **kwargs):
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
