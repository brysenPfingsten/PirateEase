import pytest
from unittest.mock import patch, MagicMock
from PirateEase.QueryHandlers.product_availability_handler import ProductAvailabilityHandler


@pytest.fixture
def handler_with_mocks():
    handler = ProductAvailabilityHandler()

    # Mock backend
    handler._backend = MagicMock()

    # Mock session
    handler._session = MagicMock()

    return handler


@patch("PirateEase.QueryHandlers.product_availability_handler.UserInterface")
def test_handle_product_availability(mock_user_interface, handler_with_mocks):
    test_item = "Golden Compass"
    mock_user_interface.get_item_name.return_value = test_item
    handler_with_mocks._backend.process_request.return_value = "We have 5 Golden Compasses in stock."

    response = handler_with_mocks.handle("Doesn't matter")

    # Assert backend call
    handler_with_mocks._backend.process_request.assert_called_once_with("inventory", test_item)

    # Assert session update
    handler_with_mocks._session.set.assert_called_once_with("item_name", test_item)

    # Assert final response
    assert response == "We have 5 Golden Compasses in stock."