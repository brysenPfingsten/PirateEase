from PirateEase.Services.exit_service import ExitService
from PirateEase.Services.inventory_service import InventoryService
from PirateEase.Services.live_agent_notifier import LiveAgentService
from PirateEase.Services.order_service import OrderService
from PirateEase.Services.refund_service import RefundService
from PirateEase.Utils.singleton import Singleton

"""
OOP Principles:
- Abstraction: BackendManager exposes a simple method process_request which hides the complexity of interacting
               with various services.
- Inheritance: Inherits from Singleton

Creational Pattern:
- Singleton: Ensures there is only one instance of BackendManager across the program for central coordination 
             and to avoid duplication.
             
Behavioral Pattern:
- Facade: process_request acts a single unified interface for multiple subsystems which simplifies client 
          interaction. This also decouples client code from the internal services which makes adding/changing
          services easier. For example, if there was a bug in one of the services, this code would not need
          to be changed.
          
SOLID Principles:
- Single Responsibility: BackendManager just coordinates request routing while each service handles its own logic.
"""


class BackendManager(Singleton):
    """
    Singleton class that manages requests to the backend.
    """

    @staticmethod
    def process_request(request_type: str, data: str = ''):
        """
        Maps request types to their respective services in the backend.
        :param request_type: The type of service you are routing a request to.
        :param data: Optional data if service you are routing to requires it.
        :return: Response from the respective service.
        """
        if request_type == "order":
            return OrderService().retrieve_order(data)
        elif request_type == "refund":
            return RefundService().refund_past_order(data)
        elif request_type == "inventory":
            return InventoryService().check_availability(data)
        elif request_type == "agent":
            return LiveAgentService().get_available_agent()
        elif request_type == "exit":
            return ExitService().get_exit_response()