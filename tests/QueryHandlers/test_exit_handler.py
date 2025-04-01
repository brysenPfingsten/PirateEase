import pytest
from unittest.mock import MagicMock
from PirateEase.QueryHandlers.exit_handler import ExitHandler


@pytest.fixture
def exit_handler_with_mock_backend():
    handler = ExitHandler()
    handler._backend = MagicMock()
    handler._backend.process_request.return_value = "Goodbye, matey!"
    return handler


def test_exit_handler_returns_exit_response(exit_handler_with_mock_backend):
    response = exit_handler_with_mock_backend.handle("Any query")

    # Assert backend was called with 'exit'
    exit_handler_with_mock_backend._backend.process_request.assert_called_once_with("exit")

    # Assert correct response was returned
    assert response == "Goodbye, matey!"
