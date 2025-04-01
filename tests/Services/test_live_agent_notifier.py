import json
import pytest
from unittest.mock import patch, mock_open
from PirateEase.Services.live_agent_notifier import Agent, LiveAgentService, LiveAgentNotifier


mock_agent_data = [
    {"name": "Captain Jack", "available": True},
    {"name": "Blackbeard", "available": False},
    {"name": "Anne Bonny", "available": True}
]


@pytest.fixture
def mock_agents_file():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_agent_data))):
        yield


@pytest.fixture
def reset_singleton():
    LiveAgentService.reset()
    LiveAgentNotifier.observers.clear()
    yield
    LiveAgentService.reset()
    LiveAgentNotifier.observers.clear()


def test_singleton_behavior(mock_agents_file, reset_singleton):
    instance1 = LiveAgentService()
    instance2 = LiveAgentService()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)


def test_initialization_loads_agents(mock_agents_file, reset_singleton):
    service = LiveAgentService()
    assert len(service._LiveAgentService__agents) == 3

    agent_names = [agent.name for agent in service._LiveAgentService__agents]
    assert "Captain Jack" in agent_names
    assert "Blackbeard" in agent_names
    assert "Anne Bonny" in agent_names


def test_available_agents_become_observers(mock_agents_file, reset_singleton):
    LiveAgentService()
    observer_names = [agent.name for agent in LiveAgentNotifier.observers]

    assert "Captain Jack" in observer_names
    assert "Anne Bonny" in observer_names
    assert "Blackbeard" not in observer_names


def test_agent_name_in_string(mock_agents_file, reset_singleton):
    service = LiveAgentService()

    assert service.agent_name_in_string("Hi Captain Jack") is True
    assert service.agent_name_in_string("Hello Anne Bonny") is True
    assert service.agent_name_in_string("No one is here") is False


@patch("PirateEase.Services.live_agent_notifier.ResponseFactory.get_response")
@patch("random.choice")
def test_get_available_agent(mock_random_choice, mock_get_response, mock_agents_file, reset_singleton):
    service = LiveAgentService()

    # Choose "Anne Bonny" as available agent
    agent_obj = next(agent for agent in service._LiveAgentService__agents if agent.name == "Anne Bonny")
    mock_random_choice.return_value = agent_obj
    mock_get_response.return_value = "Connecting you to {agent}"

    response = service.get_available_agent()

    assert "Anne Bonny" in response
    assert agent_obj.available is False
    assert agent_obj not in LiveAgentNotifier.observers
    mock_get_response.assert_called_once_with("connecting_agent")


def test_agent_alert():
    agent = Agent("Long John", True)
    history = ["Hello", "Need help!"]
    result = agent.alert(history)

    assert "Long John was alerted!" in result
    assert "History: ['Hello', 'Need help!']" in result


def test_observer_add_remove_notify():
    agent1 = Agent("Agent A", True)
    agent2 = Agent("Agent B", True)

    LiveAgentNotifier.observers.clear()
    LiveAgentNotifier.add_observer(agent1)
    LiveAgentNotifier.add_observer(agent2)

    assert agent1 in LiveAgentNotifier.observers
    assert agent2 in LiveAgentNotifier.observers

    with patch.object(agent1, 'alert') as alert1, patch.object(agent2, 'alert') as alert2:
        history = ["User asked something"]
        LiveAgentNotifier.notify_agents(history)

        alert1.assert_called_once_with(history)
        alert2.assert_called_once_with(history)

    LiveAgentNotifier.remove_observer(agent1)
    assert agent1 not in LiveAgentNotifier.observers
