import json

from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.singleton import Singleton

"""
OOP Principles
- Encapsulation: 
    - PastOrder encapsulates all order-related data.
    - RefundService contains logic for retrieving and updating refund status.
- Abstraction: Clients can just call refund_past_order and receive a response w/o needing to know how it works.
- Inheritance: RefundService inherits from Singleton.
- Composition: RefundService contains PastOrder objects.

Creational Pattern
- Singleton: Ensures only one RefundService exists so customers don't get refunded twice or more times.

SOLID Principles
- Single Responsibility:
    - PastOrder holds just the data relating to it.
    - Refund Service handles refund logic or order lookup.
- Open/Closed: Can be extended to support email confirmation, logging, etc.
- Liskov Substitution: Subclassing wouldn't break behavior.
- Interface Segregation: Only exposes one high level behavior to refund a past order.
"""


class PastOrder:
    """
    Represents an order that has already been delivered to a customer.
    """

    def __init__(self, id: int, customer_name: str, delivery_date: str, item: str, quantity: int, refunded: bool):
        self.id: int = id
        self.customer_name: str = customer_name
        self.delivery_date: str = delivery_date
        self.item: str = item
        self.quantity: int = quantity
        self.refunded: bool = refunded


class RefundService(Singleton):
    """
    Singleton class for processing refunds of past orders.
    """

    def __init__(self):
        # If already initialized, skip
        if self._initialized:
            return
        # Load past orders from DB
        with open('Databases/past_orders.json', 'r', encoding='utf-8') as f:
            raw_orders: dict = json.load(f)
            self.__orders: dict[int, PastOrder] = {
                int(order_id): PastOrder(
                    id=int(order_id),
                    customer_name=data["customer_name"],
                    delivery_date=data["delivery_date"],
                    item=data["item"],
                    quantity=data["quantity"],
                    refunded=data["refunded"]
                )
                for order_id, data in raw_orders.items()
            }
        # Mark as initialized
        self._initialized = True

    def refund_past_order(self, order_id: str) -> str:
        """
        Refunds a past order if it exists and has not already been refunded.
        :param order_id: The order ID corresponding to the past order that needs to be refunded.
        :return: Message explaining if the refund was successful, has already happened, or empty if the order did not exist.
        """
        # Lookup the order from the DB
        order: PastOrder = self.__orders.get(int(order_id))
        if order is not None:  # If the order was found
            if order.refunded:  # If the order was already refunded
                return ResponseFactory.get_response('refund_already_processed').format(order_id=order_id)
            else:  # The order was not already refunded
                order.refunded = True
                return ResponseFactory.get_response('refund_submitted').format(order_id=order_id)
        else:  # Else the order was not found
            return ''
