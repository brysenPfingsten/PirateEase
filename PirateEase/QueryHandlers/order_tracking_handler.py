from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.slow_print import slow_print
from PirateEase.Utils.user_interface import UserInterface

"""
OOP Principles
- Encapsulation: Encapsulates the full flow of order tracking logic within a single handler.
- Abstraction: Abstracts the process of getting the order ID and fetching the order details from the client code.
- Inheritance: Inherits from QueryHandler, enabling it to be used polymorphically in a query-handling system.

Behavioral Pattern
- Chain of Responsibility: Handles order-tracking queries and could delegate other queries to other handlers.
- Facade: Leverages UserInterface and BackendManager to abstract multiple subsystems behind a simple interface.

SOLID Principles
- Single Responsibility: Responsible only for managing order tracking interactions.
- Open/Closed: Can be extended to support tracking via email or phone without modifying the existing flow.
- Liskov Substitution: Can be used in place of any QueryHandler without breaking functionality.
- Interface Segregation: Only implements the handle() method needed by QueryHandler.
"""


class OrderTrackingHandler(QueryHandler):
    """
    QueryHandler for users who are requesting information about their order.
    """
    def handle(self, query: str) -> str:
        """
        If not already stored, gets an order ID from the user and tells the backend to get information about it.
        :param query: Doesn't matter
        :return: Response about the status of the order from the backend.
        """
        if 'order_id' in self._session:
            order_id: str = self._session.get('order_id')
            return self._backend.process_request('order', order_id)

        order_id: str = UserInterface.get_order_id('order_id')
        response = self._backend.process_request('order', order_id)
        while not response:
            not_found_response: str = 'PirateEase: ' + ResponseFactory.get_response('order_not_found').format(order_id=order_id)
            self._session.append_history(not_found_response)
            slow_print(not_found_response)
            order_id = UserInterface.get_order_id('order_id')
            response = self._backend.process_request('order', order_id)

        self._session.set('order_id', order_id)
        return response

