"""
OOP Principles
- Encapsulation: Logic over control of internal instances is hidden within the class.
- Abstraction: Provides a high level way of making new classes for classes that inherit.
- Inheritance: Enables other classes to inherit from this and become singletons.

Creational Pattern
- Singleton: Enforces single instances per subclass across the application which ensures shared states, avoids
             reinitializing classes, and saves memory.

SOLID Principles
- Single Responsibility: Only responsibility is to manage instance creation.
- Liskov Substitution: Subclasses of Singleton can be used interchangeably and maintain expected behavior.
- Interface Segregation: Provides only necessary functionality with __new__ and reset.
- Dependency Inversion: Does not depend on external data or services.
"""


class Singleton:
    """
    Parent class that others can inherit from to become a singleton.
    """
    # Dictionary mapping classes to their instances
    _instances: dict = {}

    def __new__(cls):
        """
        Makes a new instance if the class is not already instantiated.
        Else returns the instance that has already been instantiated.
        """
        if cls not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def reset(cls) -> None:
        """
        For testing purposes.
        :return: None
        """
        cls._instances = {}
