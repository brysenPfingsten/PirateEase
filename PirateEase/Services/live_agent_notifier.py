import json, random

from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.singleton import Singleton

"""
OOP Principles
- Encapsulation: Each class hides its internal data and behavior is contained within the classes.
- Abstraction: Clients can call get_available_agent or notify_agents w/o knowing how agents are stored or notified.
- Inheritance: LiveAgentService inherits from Singleton
- Composition: LiveAgentService is composed of Agent objects and adds agents to LiveAgentNotifier

Creational Pattern
- Singleton: Ensures a single, consistent list of agents and prevents connecting with unavailable agents.

Behavioral Pattern
- Observer: LiveAgentNotifier adds and notifies its Agent observers. This allows for dynamic subscription of agents 
            which can change as people clock in and out of work. It also decouples logic from the main service which
            makes the program more extensible.
            
SOLID Principles
- Single Responsibility
    - Agent manages its information and alerting itself.
    - LiveAgentNotifier handles observer management.
    - LiveAgentService manages agent availability and selection.
- Open/Closed: New behaviors like prioritizing more seasoned agents can be added w/o modifying existing methods
- Liskov Substitution: Subclasses of all classes could replace the base w/o breaking functionality.
- Interface Segregation: Each class exposes only necessary and relevant methods.
"""


class Agent:
    """
    Represents a human agent with a name and availability.
    """

    def __init__(self, name: str, available: bool):
        self.name: str = name
        self.available: bool = available

    def alert(self, history: list[str]):
        """
        Alerts this agent that someone is requesting assistance and gives them the history of their chat with PirateEase
        :param history: The history of the chat with PirateEase
        :return: String verifying the agent was alerted
        """
        return f'{self.name} was alerted!\nHistory: {history}'


class LiveAgentNotifier:
    """
    Class that agents can subscribe to in order to be notified of someone requesting assistance.
    """
    # All the agents subscribed to this notifier
    observers: list[Agent] = []

    @staticmethod
    def add_observer(agent: Agent) -> None:
        """
        Adds an agent to the list of observers.
        :param agent: The agent to add to the list of observers.
        :return: None
        """
        LiveAgentNotifier.observers.append(agent)

    @staticmethod
    def remove_observer(agent: Agent) -> None:
        """
        Removes an agent from the list of observers.
        :param agent: The agent to remove from the list of observers.
        :return: None
        """
        LiveAgentNotifier.observers.remove(agent)

    @staticmethod
    def notify_agents(history: list[str]) -> None:
        """
        Alerts every subscribed agent that someone is requesting assistance.
        :param history: The history from the chat with PirateEase
        :return: None
        """
        for agent in LiveAgentNotifier.observers:  # For each subscribed agent
            agent.alert(history)  # Alert them w/ history


class LiveAgentService(Singleton):
    """
    Singleton class for connecting clients with a live agent.
    """

    def __init__(self):
        # If initialized, skip
        if self._initialized:
            return
        # If not initialized, load agents from DB
        self.__agents: list[Agent] = []
        with open('Databases/agents.json', 'r', encoding='utf-8') as f:
            agents: list[dict] = json.load(f)
            for a in agents:  # For each raw agent
                agent = Agent(a.get('name'), a.get('available'))  # Instantiate an agent class
                self.__agents.append(agent)  # Add it to the list of agents
                if agent.available:  # If the agent is available
                    LiveAgentNotifier.add_observer(agent)  # Add it to the observers
        # Mark as initialized
        self._initialized = True

    def agent_name_in_string(self, s: str) -> bool:
        """
        Determines if the given string contains the name of an agent. Used to determine when to
        break out of the main loop.
        :param s: The string to check for a name in.
        :return: True if the name of an agent is found, False otherwise.
        """
        return any(agent.name in s for agent in self.__agents)

    def get_available_agent(self) -> str:
        """
        Connects the client with an available agent.
        :return: Connection string.
        """
        agent: Agent = random.choice([a for a in self.__agents if a.available])  # Choose a random agent
        agent.available = False  # Mark them as unavailable
        LiveAgentNotifier.remove_observer(agent)
        return ResponseFactory.get_response('connecting_agent').format(agent=agent.name)  # Return dynamic response
