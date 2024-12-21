from abc import abstractmethod


class AppClient:
    """
    AppClient is a singleton class that ensures the client is initialized only once.
    Setups, inits are async to make sure runtime is not blocked by any singular client.
    """

    _instances = {}  # Store instances per class
    _locks = {}  # Store locks per class

    def __init__(self):
        self.client = None

    async def get_client(self):
        if self.client is None:
            await self._setup()
        return self.client

    @abstractmethod
    async def _setup(self):
        pass

    """Singleton Pattern"""

    @classmethod
    async def instance(cls):
        # Initialize class-specific tracking if not exists
        if cls not in cls._instances:
            cls._locks[cls] = False
            cls._instances[cls] = None

        if cls._instances[cls] is None:
            if cls._locks[cls]:
                raise RuntimeError(
                    f"Instance of {cls.__name__} is being initialized; cannot reinitialize."
                )
            cls._locks[cls] = True
            cls._instances[cls] = cls()
            await cls._instances[cls]._setup()

        return cls._instances[cls]

    def __new__(cls, *args, **kwargs):
        # Prevent direct instantiation
        if cls._instances.get(cls) is not None:
            raise RuntimeError(
                f"{cls.__name__} is a singleton. Use {cls.__name__}.instance() instead."
            )
        return super().__new__(cls)

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            return self.instance(*args, **kwargs)
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
