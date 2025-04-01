from unittest.mock import mock_open, patch

import pytest
from PirateEase.QueryHandlers.query_manager import QueryManager
from PirateEase.QueryHandlers.order_tracking_handler import OrderTrackingHandler
from PirateEase.QueryHandlers.refund_handler import RefundHandler
from PirateEase.QueryHandlers.product_availability_handler import ProductAvailabilityHandler
from PirateEase.QueryHandlers.live_agent_handler import LiveAgentHandler
from PirateEase.QueryHandlers.exit_handler import ExitHandler
from PirateEase.QueryHandlers.query_database import QueryDatabase
from PirateEase.QueryHandlers.default_handler import DefaultHandler


@pytest.fixture
def manager():
    with patch('builtins.open', mock_open(read_data='[]')):
        yield QueryManager()


@pytest.mark.parametrize(
    "query_type,expected_type",
    [
        ("order", OrderTrackingHandler),
        ("refund", RefundHandler),
        ("inventory", ProductAvailabilityHandler),
        ("live_agent", LiveAgentHandler),
        ("exit", ExitHandler),
        ("db", QueryDatabase),
        ("unknown", DefaultHandler),
        ("ReFuNd", RefundHandler),
    ]
)
def test_get_handler_returns_correct_instance(manager, query_type, expected_type):
    handler = manager.get_handler(query_type)
    assert isinstance(handler, expected_type)


def test_get_handler_invalid_type_returns_none(manager):
    handler = manager.get_handler("parrot")
    assert handler is None
