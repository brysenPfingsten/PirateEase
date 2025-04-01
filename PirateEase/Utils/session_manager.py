from PirateEase.Utils.singleton import Singleton

"""
OOP Principles
- Encapsulation: The internal state and history and hidden behind getters and setters.
- Abstraction: Methods like get, set, and append_history abstracts how data is stored and manipulated.
- Inheritance: Inherits from Singleton

Creation Pattern
- Singleton: Ensures a global and centralized state for consistency across services and handlers.

SOLID Principles
- Single Responsibility: Manages session state and history only.
- Open/Closed: Can be extended w/o modifying existing methods
- Interface Segregation: Provides a focused interface for operations on the session state and history
- Dependency Inversion: Does not depend on external data or services. 
"""


class SessionManager(Singleton):
    """
    Singleton class for managing the history of chats and any information gathered during the conversation.
    """

    def __init__(self):
        """
        If not already initialized, a new session will be created with an empty dictionary.
        """
        if self._initialized:
            return
        self.__state: dict[str, str] = {}
        self.__history: list[str] = []
        self._initialized = True

    @property
    def state(self) -> dict[str, any]:
        return self.__state

    @property
    def history(self) -> list[str]:
        return self.__history

    def __contains__(self, item: str) -> bool:
        """
        Simplifies interacting with a SessionManager by allowing a user to ask if some key is in it.
        E.g. if 'order_id' in self._session.
        :param item: The item you are checking for in the state.
        :return: True if the item is in the state, False otherwise.
        """
        return item in self.__state

    def get(self, key: str, default=None) -> str | None:
        """
        Simplifies interacting with a SessionManager by allowing a user to get something from its state.
        :param key: The key into the state you want to get.
        :param default: Default value to return if the key is not in the state.
        :return: Value for the given key if it exists in the state, default value otherwise.
        """
        return self.__state.get(key, default)

    def set(self, key: str, value) -> None:
        """
        Simplifies interacting with a SessionManager by allowing a user to set something in its state.
        :param key: The key into the state you want to set.
        :param value: The value to want to associate with the given key.
        :return: None
        """
        self.__state[key] = value

    def append_history(self, message: str) -> None:
        """
        Appends a message to the history of this session.
        :param message: The message you want to add to the history.
        :return: None
        """
        self.__history.append(message)
