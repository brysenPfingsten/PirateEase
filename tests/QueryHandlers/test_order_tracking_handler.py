import pytest
from unittest.mock import patch, MagicMock
from PirateEase.QueryHandlers.order_tracking_handler import OrderTrackingHandler


@pytest.fixture
def handler_with_mocks():
    handler = OrderTrackingHandler()

    # Mock backend
    handler._backend = MagicMock()

    # Mock session
    handler._session = MagicMock()
    handler._session.__contains__.side_effect = lambda key: key == 'order_id'
    handler._session.get.return_value = "42"

    return handler


def test_handle_with_existing_order_id(handler_with_mocks):
    handler_with_mocks._backend.process_request.return_value = "Order #42 will arrive tomorrow!"

    result = handler_with_mocks.handle("any query")

    handler_with_mocks._session.get.assert_called_once_with("order_id")
    handler_with_mocks._backend.process_request.assert_called_once_with("order", "42")
    assert result == "Order #42 will arrive tomorrow!"


@patch("PirateEase.QueryHandlers.order_tracking_handler.UserInterface")
@patch("PirateEase.QueryHandlers.order_tracking_handler.ResponseFactory")
@patch("PirateEase.QueryHandlers.order_tracking_handler.slow_print")
def test_handle_with_missing_order_id_and_retry(
    mock_slow_print, mock_response_factory, mock_user_interface
):
    handler = OrderTrackingHandler()

    handler._session = MagicMock()
    handler._session.__contains__.return_value = False
    handler._session.append_history = MagicMock()
    handler._session.set = MagicMock()

    handler._backend = MagicMock()
    handler._backend.process_request.side_effect = ['', 'Order #99 is on the way!']

    mock_user_interface.get_order_id.side_effect = ["99", "99"]
    mock_response_factory.get_response.return_value = "Order #{order_id} not found."

    result = handler.handle("any query")

    # Assert final output
    assert result == "Order #99 is on the way!"

    # Confirm backend was retried
    assert handler._backend.process_request.call_count == 2

    # Confirm prompt was called twice
    assert mock_user_interface.get_order_id.call_count == 2

    # Confirm slow_print got the fallback
    mock_slow_print.assert_called_once_with("PirateEase: Order #99 not found.")

    # Check session history was updated in order
    history_calls = handler._session.append_history.call_args_list
    assert len(history_calls) == 1
    assert history_calls[0][0][0] == "PirateEase: Order #99 not found."

    # Confirm session was updated with final successful ID
    handler._session.set.assert_called_once_with("order_id", "99")
