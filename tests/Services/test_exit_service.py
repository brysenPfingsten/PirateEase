import pytest
from unittest.mock import patch
from PirateEase.Services.exit_service import ExitService


@pytest.fixture
def mock_response_factory():
    with patch('PirateEase.Services.exit_service.ResponseFactory') as mock:
        yield mock


def test_singleton_behavior():
    instance1 = ExitService()
    instance2 = ExitService()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)


def test_get_exit_response(mock_response_factory):
    # Setup mock response
    mock_response_factory.get_response.return_value = "Goodbye, thanks for using PirateEase!"

    # Test the method
    result = ExitService.get_exit_response()

    # Verify calls and result
    mock_response_factory.get_response.assert_called_once_with("exit")
    assert result == "Goodbye, thanks for using PirateEase!"


def test_get_exit_response_different_responses(mock_response_factory):
    # First test with one response
    mock_response_factory.get_response.return_value = "Farewell, matey!"
    assert ExitService.get_exit_response() == "Farewell, matey!"

    # Change mock response and test again
    mock_response_factory.get_response.return_value = "Until next time!"
    assert ExitService.get_exit_response() == "Until next time!"

    # Verify two calls were made
    assert mock_response_factory.get_response.call_count == 2
    mock_response_factory.get_response.assert_called_with("exit")


def test_initialization():
    instance = ExitService()
    assert hasattr(instance, '_initialized')
    assert instance._initialized


def test_reset_behavior(mock_response_factory):
    # Get initial instance
    instance1 = ExitService()

    # Reset the singleton
    ExitService.reset()

    # Get new instance
    instance2 = ExitService()

    # Verify new instance
    assert instance1 is not instance2
    assert hasattr(instance2, '_initialized')

    # Test method still works
    mock_response_factory.get_response.return_value = "Test message"
    assert ExitService.get_exit_response() == "Test message"