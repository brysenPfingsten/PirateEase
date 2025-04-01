from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.singleton import Singleton

"""
OOP Principles
- Encapsulation: Encapsulates the logic of producing an exit response.
- Abstraction: Provides a simple method to return an exit response w/o exposing how or where the response is retrieved.
- Inheritance: Inherits from Singleton.

Creational Pattern
- Singleton: Ensures only one ExitService exists throughout the lifecyle which saves resources and ensures
            consistent behavior.

SOLID Principles
- Single Responsibility: Only exists to handle exit-related logic like returning responses
- Liskov Substitution: Could be subclassed to support for complex behavior.
- Interface Segregation: get_exit_response is the only exposed method
"""


class ExitService(Singleton):
    """
    Singleton class for dynamically generating exit messages.
    """

    def __init__(self):
        self._initialized = True

    @staticmethod
    def get_exit_response():
        """
        Dynamically retrieves an exit message from the response factory.
        :return: Farewell message.
        """
        return ResponseFactory.get_response("exit")