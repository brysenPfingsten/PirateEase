import json

from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.singleton import Singleton

"""
OOP Principles
- Encapsulation:
    - Order encapsulates all the information relevant to an order and its formatting logic.
    - OrderService contains logic to retrieve order information.
- Abstraction: retrieve_order gives a simple interface for getting order info while hiding how it is done.
- Inheritance: OrderService inherits from Singleton
- Composition: OrderService is composed of many Order objects.

Creational Pattern
- Singleton: Ensures a single source of truth for all order data so there is no desync and avoids loading and parsing
             the same data multiple times.
             
SOLID Principles
- Single Responsibility:
    - Order holds and formats order data.
    - OrderService handles loading and retrieving orders.
- Open/Closed: Can be extended to add filtering for specific regions or something similar w/o modifying core logic.
- Liskov Substitution: Subclassing wouldn't break behavior.
- Interface Segregation: The classes expose only focused and necessary interfaces.
"""


class Order:
    """
    Represents an outgoing order within this business.
    """

    def __init__(self, id: int, customer_name: str, order_date: str, eta_hours: int, item: str, quantity: int,
                 refunded: bool):
        self.id: int = id
        self.customer_name: str = customer_name
        self.order_date: str = order_date
        self.eta_hours: int = eta_hours
        self.item: str = item
        self.quantity: int = quantity
        self.refunded: bool = refunded

    def __str__(self):
        """
        Returns a string representation of this order.
        :return: String representation of this order.
        """
        return ResponseFactory.get_response('order_arrival').format(order_id=self.id, customer_name=self.customer_name,
                                                                    days=round(self.eta_hours / 24, 1))


class OrderService(Singleton):
    """
    Singleton class that retrieves information about an outgoing order.
    """

    def __init__(self):
        # If already initialized, skip
        if self._initialized:
            return
        # Load orders from DB
        with open('Databases/orders.json', 'r', encoding='utf-8') as f:
            raw_orders: dict = json.load(f)
            self.__orders: dict[int, Order] = {
                int(order_id): Order(
                    id=int(order_id),
                    customer_name=data["customer_name"],
                    order_date=data["order_date"],
                    eta_hours=data["eta_hours"],
                    item=data["item"],
                    quantity=data["quantity"],
                    refunded=False
                )
                for order_id, data in raw_orders.items()
            }
        # Mark as initialized
        self._initialized = True

    def retrieve_order(self, order_id: str) -> str:
        """
        Gets the order corresponding to the given order id.
        :param order_id: The id of the order to retrieve.
        :return: String representation of the order or empty string if no order is found.
        """
        # Get the order from the db
        order: Order = self.__orders.get(int(order_id))
        if order is not None:  # If an order matched
            return str(order)  # Return its string representation
        else:  # No order matched the order ID
            return ''  # Return an empty string
