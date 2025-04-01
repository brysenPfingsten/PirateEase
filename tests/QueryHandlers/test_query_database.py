import pytest
import json
from unittest.mock import patch, mock_open
from PirateEase.QueryHandlers.query_database import QueryDatabase


@pytest.fixture
def sample_query_db():
    return {
        "how do i order?": "To order, simply type what you want!",
        "what’s your refund policy?": "Refunds are available within 30 days of delivery.",
        "hello": "Ahoy there, matey!"
    }


@pytest.fixture
def mock_queries_file(sample_query_db):
    mock_data = json.dumps(sample_query_db)
    m = mock_open(read_data=mock_data)
    with patch("builtins.open", m):
        yield


def test_known_query_returns_response(mock_queries_file):
    handler = QueryDatabase()
    result = handler.handle("How do I order?")
    assert result == "To order, simply type what you want!"


def test_unknown_query_returns_empty_string(mock_queries_file):
    handler = QueryDatabase()
    result = handler.handle("Do you sell parrots?")
    assert result == ''
