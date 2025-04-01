from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.slow_print import slow_print
from PirateEase.Utils.user_interface import UserInterface

"""
OOP Principles
- Encapsulation: Encapsulates the refund interaction flow including input, validation, and response generation.
- Abstraction: Hides the complexities of refund processing behind a single handle() method.
- Inheritance: Inherits from QueryHandler, enabling polymorphism in a query-handling system.

Behavioral Pattern
- Chain of Responsibility: Participates in a handler chain to process refund-related queries.

Structural Pattern
- Facade: Leverages UserInterface and BackendManager to interact with the user and backend systems through simple interfaces.

SOLID Principles
- Single Responsibility: Only handles refund-related user interaction and backend communication.
- Open/Closed: Can be extended with additional refund logic (e.g., reason categorization or email confirmation) without modifying core logic.
- Liskov Substitution: Can be used in place of any QueryHandler without breaking the system.
- Interface Segregation: Only implements the handle() method required by QueryHandler.
"""

class RefundHandler(QueryHandler):
    """
    QueryHandler for users who are requesting a refund.
    """
    def handle(self, query: str) -> str:
        """
        If it doesn't already exist, gets the refund_id from the user and a refund reason then directs
        the backend to refund the order.
        :param query: Doesn't matter
        :return: Final response indicating if the order was refunded or not.
        """
        refund_id: str = ''
        if 'refund_id' in self._session:
            refund_id = self._session.get('refund_id')
            return self._backend.process_request('refund_id', refund_id)
        else:
            refund_id = UserInterface.get_order_id('refund_id')
            response = self._backend.process_request('refund', refund_id)
            while not response:
                not_found_response: str = 'PirateEase: ' + ResponseFactory.get_response('order_not_found').format(order_id=refund_id)
                self._session.append_history(not_found_response)
                slow_print(not_found_response)
                refund_id = UserInterface.get_order_id('refund_id')
                response = self._backend.process_request('refund', refund_id)
            self._session.set('refund_id', refund_id)
            UserInterface.get_refund_reason()
            return response
