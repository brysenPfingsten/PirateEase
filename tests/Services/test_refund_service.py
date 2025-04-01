import pytest
import json
from unittest.mock import patch, mock_open
from PirateEase.Services.refund_service import RefundService, PastOrder


@pytest.fixture
def sample_past_orders():
    return {
        "101": {
            "customer_name": "Davy Jones",
            "delivery_date": "2025-03-25",
            "item": "Spyglass",
            "quantity": 1,
            "refunded": False
        },
        "102": {
            "customer_name": "Calypso",
            "delivery_date": "2025-03-26",
            "item": "Map Scroll",
            "quantity": 3,
            "refunded": True
        }
    }


@pytest.fixture
def mock_past_orders_file(sample_past_orders):
    mock_data = json.dumps(sample_past_orders)
    m = mock_open(read_data=mock_data)
    with patch("builtins.open", m):
        yield


@pytest.fixture
def mock_response_factory():
    with patch("PirateEase.Services.refund_service.ResponseFactory") as mock:
        mock.get_response.side_effect = lambda key: {
            "refund_submitted": "Refund for order #{order_id} submitted.",
            "refund_already_processed": "Refund for order #{order_id} was already processed."
        }[key]
        yield mock


@pytest.fixture(autouse=True)
def reset_singleton():
    RefundService.reset()
    yield
    RefundService.reset()


def test_singleton_behavior(mock_past_orders_file):
    instance1 = RefundService()
    instance2 = RefundService()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)


def test_successful_refund(mock_past_orders_file, mock_response_factory):
    service = RefundService()
    result = service.refund_past_order("101")

    assert result == "Refund for order #101 submitted."
    order = service._RefundService__orders[101]
    assert order.refunded is True
    mock_response_factory.get_response.assert_called_with("refund_submitted")


def test_already_refunded(mock_past_orders_file, mock_response_factory):
    service = RefundService()
    result = service.refund_past_order("102")

    assert result == "Refund for order #102 was already processed."
    order = service._RefundService__orders[102]
    assert order.refunded is True
    mock_response_factory.get_response.assert_called_with("refund_already_processed")


def test_nonexistent_order(mock_past_orders_file, mock_response_factory):
    service = RefundService()
    result = service.refund_past_order("999")

    assert result == ''
    mock_response_factory.get_response.assert_not_called()


def test_order_initialization(mock_past_orders_file):
    service = RefundService()
    orders = service._RefundService__orders

    assert isinstance(orders[101], PastOrder)
    assert orders[101].item == "Spyglass"
    assert orders[102].refunded is True
