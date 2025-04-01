from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.QueryHandlers.default_handler import DefaultHandler
from PirateEase.QueryHandlers.exit_handler import ExitHandler
from PirateEase.QueryHandlers.live_agent_handler import LiveAgentHandler
from PirateEase.QueryHandlers.order_tracking_handler import OrderTrackingHandler
from PirateEase.QueryHandlers.product_availability_handler import ProductAvailabilityHandler
from PirateEase.QueryHandlers.refund_handler import RefundHandler
from PirateEase.QueryHandlers.query_database import QueryDatabase

"""
OOP Principles
- Encapsulation: Encapsulates the mapping and instantiation of query handlers within a single coordinating class.
- Abstraction: Clients only need to call get_handler() without knowing how handlers are managed or created.
- Polymorphism: Each handler conforms to the QueryHandler interface, allowing them to be used interchangeably.

Creational Pattern
- Factory Pattern: Dynamically returns the correct handler based on the input query type, decoupling instantiation from usage.

SOLID Principles
- Single Responsibility: Manages the creation and lookup of handlers only—does not handle query execution.
- Open/Closed: New handlers can be added to the dictionary without modifying the rest of the logic.
- Liskov Substitution: All handlers returned implement the QueryHandler interface, ensuring substitutability.
- Interface Segregation: Returns objects that conform to a clean, minimal interface.
"""

class QueryManager:
    """
    Dynamically retrieves QueryHandlers based on the type
    """
    def __init__(self):
        self.handlers: dict[str, QueryHandler] = {
            "order": OrderTrackingHandler(),
            "refund": RefundHandler(),
            "inventory": ProductAvailabilityHandler(),
            "live_agent": LiveAgentHandler(),
            "exit": ExitHandler(),
            "db": QueryDatabase(),
            "unknown": DefaultHandler()
        }

    def get_handler(self, query_type: str) -> QueryHandler:
        """
        Retrieves the handler corresponding to the given query_type
        :param query_type: The type of query you need a handler for.
        :return: QueryHandler matching the given query_type
        """
        return self.handlers.get(query_type.lower())