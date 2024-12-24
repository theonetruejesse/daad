from abc import abstractmethod


class AppClient:
    """
    AppClient is a singleton class that ensures the client is initialized only once.
    Setups are async to make sure runtime is not blocked by any singular client.
    This class should be treated as a configuration layer.
    """

    _instance = None  # Single instance for all clients
    _initialized_classes = set()  # Track which classes have been initialized

    @abstractmethod
    async def _setup(self):
        pass

    """Singleton Pattern"""

    @classmethod
    async def instance(cls):
        print(f"Getting instance of {cls.__name__}")
        if not AppClient._instance:
            print(f"Creating instance of {cls.__name__}")
            AppClient._instance = cls()

        if cls not in AppClient._initialized_classes:
            print(f"Initializing {cls.__name__}")
            AppClient._initialized_classes.add(cls)
            await AppClient._instance._setup()

        return AppClient._instance

    def __new__(cls, *args, **kwargs):
        if AppClient._instance is not None:
            raise RuntimeError(
                f"{cls.__name__} is a singleton. Use {cls.__name__}.instance() instead."
            )
        return super().__new__(cls)

    def __call__(self, *args, **kwargs):
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self.__class__)
