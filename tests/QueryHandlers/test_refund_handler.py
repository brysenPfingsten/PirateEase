import pytest
from unittest.mock import patch, MagicMock
from PirateEase.QueryHandlers.refund_handler import RefundHandler


@pytest.fixture
def handler_with_mocks():
    handler = RefundHandler()
    handler._session = MagicMock()
    handler._backend = MagicMock()
    return handler


def test_handle_uses_existing_refund_id(handler_with_mocks):
    handler_with_mocks._session.__contains__.return_value = True
    handler_with_mocks._session.get.return_value = "123"
    handler_with_mocks._backend.process_request.return_value = "Refund for order #123 submitted."

    result = handler_with_mocks.handle("anything")
    assert result == "Refund for order #123 submitted."
    handler_with_mocks._backend.process_request.assert_called_once_with('refund_id', '123')


@patch("PirateEase.QueryHandlers.refund_handler.ResponseFactory")
@patch("PirateEase.QueryHandlers.refund_handler.UserInterface")
@patch("PirateEase.QueryHandlers.refund_handler.slow_print")
def test_handle_prompts_until_valid_refund_id(
    mock_slow_print, mock_user_interface, mock_response_factory, handler_with_mocks
):
    handler_with_mocks._session.__contains__.return_value = False
    handler_with_mocks._session.append_history = MagicMock()
    handler_with_mocks._session.set = MagicMock()

    # Backend fails first time, then succeeds
    handler_with_mocks._backend.process_request.side_effect = ["", "Refund complete!"]

    # Simulate user entering same refund ID twice
    mock_user_interface.get_order_id.side_effect = ["999", "999"]
    mock_user_interface.get_refund_reason.return_value = "Item was damaged"
    mock_response_factory.get_response.return_value = "Order #{order_id} not found."

    result = handler_with_mocks.handle("any query")

    # Final result should be the success string
    assert result == "Refund complete!"

    # UserInterface.get_order_id called twice
    assert mock_user_interface.get_order_id.call_count == 2

    # Backend called twice (once fail, once success)
    assert handler_with_mocks._backend.process_request.call_count == 2
    handler_with_mocks._backend.process_request.assert_called_with("refund", "999")

    # Session.set called with correct refund_id
    handler_with_mocks._session.set.assert_called_once_with("refund_id", "999")

    # Refund reason asked
    mock_user_interface.get_refund_reason.assert_called_once()

    # Check session history entries
    history_calls = handler_with_mocks._session.append_history.call_args_list
    assert len(history_calls) == 1
    assert history_calls[0][0][0] == "PirateEase: Order #999 not found."

    # slow_print called with correct message
    mock_slow_print.assert_called_once_with("PirateEase: Order #999 not found.")
