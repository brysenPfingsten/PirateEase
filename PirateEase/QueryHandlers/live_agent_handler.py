from PirateEase.Services.live_agent_notifier import LiveAgentService, LiveAgentNotifier
from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.Utils.response_factory import ResponseFactory

"""
OOP Principles
- Encapsulation: Encapsulates the logic for notifying agents and generating a response in a single handler.
- Abstraction: The caller doesn't need to know how agents are notified or selected.
- Inheritance: Inherits from QueryHandler, allowing it to fit seamlessly into the handler chain.

Behavioral Pattern
- Chain of Responsibility: Handles live-agent escalation queries within a chain of handlers. Other handlers can be used for different intents.
- Observer: Uses LiveAgentNotifier to notify multiple Agent observers when escalation is triggered.

SOLID Principles
- Single Responsibility: Manages only the escalation process to a live agent.
- Open/Closed: Can be extended to support prioritization, logging, or agent confirmation without modifying the core logic.
- Liskov Substitution: Can replace any QueryHandler without affecting the system.
- Interface Segregation: Only implements the handle() method required by the interface.
"""


class LiveAgentHandler(QueryHandler):
    """
    QueryHandler for people requesting a live agent.
    """

    def handle(self, query=None) -> str:
        """
        Dynamically generates a response to the agent request and tells the backend to connect the user
        with a live agent.
        :param query: Doesn't matter
        :return: Dynamically generated response and agent connection string.
        """
        LiveAgentNotifier.notify_agents(self._session.state)

        chat_response: str = f'PirateEase: {ResponseFactory.get_response("live_agent")}'
        agent_connection_response: str = self._backend.process_request('agent')
        return chat_response + '\n' + agent_connection_response
