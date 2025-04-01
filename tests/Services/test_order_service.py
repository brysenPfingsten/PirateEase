import pytest
import json
from unittest.mock import patch, mock_open
from PirateEase.Services.order_service import OrderService, Order


@pytest.fixture
def sample_orders():
    return {
        "1": {
            "customer_name": "Elizabeth",
            "order_date": "2025-03-30",
            "eta_hours": 48,
            "item": "Cutlass",
            "quantity": 2
        },
        "2": {
            "customer_name": "Will",
            "order_date": "2025-03-28",
            "eta_hours": 24,
            "item": "Compass",
            "quantity": 1
        }
    }


@pytest.fixture
def mock_orders_file(sample_orders):
    mock_data = json.dumps(sample_orders)
    m = mock_open(read_data=mock_data)
    with patch("builtins.open", m):
        yield


@pytest.fixture
def mock_response_factory():
    with patch("PirateEase.Services.order_service.ResponseFactory") as mock:
        mock.get_response.return_value = "Order #{order_id} for {customer_name} will arrive in {days} days."
        yield mock


@pytest.fixture(autouse=True)
def reset_singleton():
    OrderService.reset()
    yield
    OrderService.reset()


def test_singleton_behavior(mock_orders_file):
    instance1 = OrderService()
    instance2 = OrderService()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)


def test_order_initialization(mock_orders_file):
    service = OrderService()
    orders = service._OrderService__orders

    assert len(orders) == 2
    assert 1 in orders
    assert isinstance(orders[1], Order)
    assert orders[1].customer_name == "Elizabeth"


def test_retrieve_existing_order(mock_orders_file, mock_response_factory):
    service = OrderService()

    response = service.retrieve_order("1")

    mock_response_factory.get_response.assert_called_once_with("order_arrival")
    assert "Order #1 for Elizabeth will arrive in 2.0 days." in response


def test_retrieve_nonexistent_order(mock_orders_file):
    service = OrderService()

    response = service.retrieve_order("999")
    assert response == ''


def test_order_str(mock_response_factory):
    order = Order(
        id=42,
        customer_name="Jack",
        order_date="2025-03-31",
        eta_hours=36,
        item="Rum Barrel",
        quantity=5,
        refunded=False
    )

    result = str(order)

    mock_response_factory.get_response.assert_called_once_with("order_arrival")
    assert "Order #42 for Jack will arrive in 1.5 days." in result