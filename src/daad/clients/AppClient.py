from abc import abstractmethod


class AppClient:
    """
    Each subclass has exactly one instance.
    """

    _instances = {}
    _initialized_classes = set()

    @abstractmethod
    async def _setup(self):
        pass

    @abstractmethod
    async def cleanup(self):
        pass

    @classmethod
    async def instance(cls, *args, **kwargs):
        # print(f"Initializing {cls.__name__}")
        # 1) Create instance if none yet
        if cls not in cls._instances:
            # print(f"Creating {cls.__name__}")
            obj = super(AppClient, cls).__new__(cls)
            obj.__init__(*args, **kwargs)  # <-- manually call __init__
            cls._instances[cls] = obj

        # 2) Run _setup if not done
        if cls not in cls._initialized_classes:
            # print(f"Running {cls.__name__} setup")
            cls._initialized_classes.add(cls)
            await cls._instances[cls]._setup()

        # print(f"Returning {cls.__name__}")
        return cls._instances[cls]

    def __new__(cls, *args, **kwargs):
        # Only allow creation if we don't have one stored
        if cls in cls._instances:
            raise RuntimeError(
                f"{cls.__name__} already instantiated. Use {cls.__name__}.instance()"
            )
        return super().__new__(cls)

    def __call__(self, *args, **kwargs):
        raise TypeError("Singletons must be accessed through .instance().")

    def __instancecheck__(self, inst):
        return isinstance(inst, self.__class__)
