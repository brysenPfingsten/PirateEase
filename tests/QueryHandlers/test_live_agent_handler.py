import pytest
from unittest.mock import patch, MagicMock
from PirateEase.QueryHandlers.live_agent_handler import LiveAgentHandler


@pytest.fixture
def handler_with_mocks():
    handler = LiveAgentHandler()

    # Mock session state
    handler._session = MagicMock()
    handler._session.state = ["previous message", "another message"]

    # Mock backend
    handler._backend = MagicMock()
    handler._backend.process_request.return_value = "Connecting you to Blackbeard..."

    return handler


@patch("PirateEase.QueryHandlers.live_agent_handler.ResponseFactory")
@patch("PirateEase.QueryHandlers.live_agent_handler.LiveAgentNotifier")
def test_handle_triggers_agent_connection(mock_notifier, mock_factory, handler_with_mocks):
    mock_factory.get_response.return_value = "A live agent will be with you shortly."

    response = handler_with_mocks.handle("Help me!")

    # Check LiveAgentNotifier was called with session history
    mock_notifier.notify_agents.assert_called_once_with(["previous message", "another message"])

    # Check response was composed correctly
    expected = (
        "PirateEase: A live agent will be with you shortly.\n"
        "Connecting you to Blackbeard..."
    )
    assert response == expected

    # Check response factory usage
    mock_factory.get_response.assert_called_once_with("live_agent")
    handler_with_mocks._backend.process_request.assert_called_once_with("agent")
