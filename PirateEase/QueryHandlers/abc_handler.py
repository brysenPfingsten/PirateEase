from abc import ABC, abstractmethod

from PirateEase.Utils.backend_manager import BackendManager
from PirateEase.Utils.session_manager import SessionManager

"""
OOP Principles
- Encapsulation: Access to BackendManager and SessionManager for subclasses.
- Inheritance: Inherits from ABC and is destined to be inherited from.
- Abstraction: Defines an abstract interface for all query handles to implement in their own ways.

Behavioral Pattern
- Chain of Responsibility: Abstract handle method allows subclasses to participate in a query handling chain

SOLID Principles
- Single Responsibility: Provides a single base interface for handling queries.
- Open/Closed: New handler types can be added by subclassing w/o modifying this class.
- Liskov Substitution: Any subclass of QueryHandler can stand in place for a QueryHandler and be used polymorphically.
- Interface Segregation: Minimal and purpose driven interface with just one method.
"""


class QueryHandler(ABC):
    """
    Abstract class for handling queries.
    """

    def __init__(self):
        # Each handler has access to the same backend manager and session manager
        self._backend = BackendManager()
        self._session = SessionManager()

    @abstractmethod
    def handle(self, query: str) -> str:
        """
        Abstract method for handling queries.
        :param query: The query to handle.
        :return: Final response to the query.
        """
        pass
