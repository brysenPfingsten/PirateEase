from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.Utils.user_interface import UserInterface

"""
OOP Principles
- Encapsulation: Encapsulates the logic for retrieving item name and checking inventory within a single handler.
- Abstraction: Hides the details of how the item is obtained and how inventory is checked.
- Inheritance: Inherits from QueryHandler, allowing it to work within a polymorphic handler system.

Behavioral Pattern
- Chain of Responsibility: Handles product availability queries as part of a larger handler chain.
- Facade: Uses UserInterface and BackendManager to simplify interaction with input/output and backend services.

SOLID Principles
- Single Responsibility: Focuses solely on handling product availability queries.
- Open/Closed: Can be extended to support fuzzy matching, multiple items, or filtering without changing existing logic.
- Liskov Substitution: Fully substitutable for any other QueryHandler implementation.
- Interface Segregation: Only implements the handle() method required by the interface.
"""


class ProductAvailabilityHandler(QueryHandler):
    """
    QueryHandler for users requesting information about products.
    """

    def handle(self, query) -> str:
        """
        Gets the item name from the user and tells the backend to get information about it.
        :param query: Doesn't matter
        :return: Response from the backend with information about the product.
        """
        item_name: str = UserInterface.get_item_name()
        self._session.set('item_name', item_name)
        return self._backend.process_request('inventory', item_name)
