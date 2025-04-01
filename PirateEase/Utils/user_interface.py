from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.session_manager import SessionManager
from PirateEase.Utils.slow_print import slow_print

"""
OOP Principles
- Encapsulation: The logic to interact with users is internal and encapsulated within clear methods.
- Abstraction: Users don't need to know how the message are obtained or where the history is stored.
- Inheritance: Uses composition to manage session information.

Structural Pattern
- Facade: Provides a simple interface that interfaces with things like ResponseFactory and SessionManager.

SOLID Principles
- Single Responsibility: Handles user interaction only.
- Liskov Substitution: Could be subclassed with more advanced features.
- Interface Segregation: Exposes only necessary methods.
"""


class UserInterface:
    """
    Class for collecting and validating input from the user.
    """
    session: SessionManager = SessionManager()

    @classmethod
    def get_order_id(cls, order_or_refund_id: str) -> str:
        """
        Gets an order ID from the user.
        :param order_or_refund_id: either 'order_id' or 'refund_id'
        :return: The collected order ID.
        """
        while True:
            message: str = 'PirateEase: ' + ResponseFactory.get_response(order_or_refund_id)
            slow_print(message)
            cls.session.append_history(message)
            order_id: str = input('User: ').strip()
            try:
                cls.session.append_history(f'User: {order_id}')  # Store as string
                int(order_id)  # Validate it's numeric
                return order_id
            except ValueError:
                error_msg: str = ResponseFactory.get_response('invalid_order_id')
                cls.session.append_history(error_msg)
                slow_print(error_msg)

    @classmethod
    def get_item_name(cls) -> str:
        """
        Gets an item name from the user.
        :return: The collected item name.
        """
        message: str = 'PirateEase: ' + ResponseFactory.get_response('product')
        slow_print(message)
        cls.session.append_history(message)
        item_name: str = input('User: ').strip()
        cls.session.append_history(f'User: {item_name}')
        return item_name

    @classmethod
    def get_refund_reason(cls):
        """
        Gets a refund reason from the user.
        :return: The collected refund reason.
        """
        message: str = 'PirateEase: ' + ResponseFactory.get_response('refund_reason')
        slow_print(message)
        cls.session.append_history(message)
        refund_reason: str = input('User: ').strip()
        cls.session.append_history(f'User: {refund_reason}')
        return refund_reason
