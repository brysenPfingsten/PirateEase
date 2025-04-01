import pytest
from unittest.mock import patch, mock_open
from PirateEase.QueryHandlers.default_handler import DefaultHandler


@pytest.fixture
def mock_response_factory():
    with patch("PirateEase.QueryHandlers.default_handler.ResponseFactory") as mock:
        mock.get_response.return_value = "Sorry, I didn’t understand that."
        yield mock


def test_handle_logs_query_and_returns_response(mock_response_factory):
    handler = DefaultHandler()
    fake_query = "Where's me treasure?"

    m = mock_open()
    with patch("builtins.open", m):
        result = handler.handle(fake_query)

    # Assert query was written to file
    m.assert_called_once_with("Databases/unrecognized_queries.txt", "a", encoding="utf-8")
    handle = m()
    handle.write.assert_called_once_with(fake_query + '\n')

    # Assert proper fallback response
    assert result == "Sorry, I didn’t understand that."
    mock_response_factory.get_response.assert_called_once_with("default")
