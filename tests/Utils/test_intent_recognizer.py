from unittest.mock import mock_open
from PirateEase.Utils.intent_recognizer import IntentRecognizer


def test_recognize_intent_with_matching_phrase(mocker):
    # Mock the JSON data
    mock_data = {
        "order": ["order", "buy", "purchase"],
        "refund": ["refund", "return"],
    }
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=mock_data)

    recognizer = IntentRecognizer()

    # Test matching phrases
    assert recognizer.recognize_intent("I want to buy something") == "order"
    assert recognizer.recognize_intent("Can I return this?") == "refund"


def test_recognize_intent_with_no_match(mocker):
    # Mock the JSON data
    mock_data = {
        "order": ["order", "buy"],
        "refund": ["refund"],
    }
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=mock_data)

    recognizer = IntentRecognizer()

    # Test non-matching phrases
    assert recognizer.recognize_intent("How do I track my package?") == "unknown"
    assert recognizer.recognize_intent("") == "unknown"


def test_recognize_intent_case_insensitive(mocker):
    # Mock the JSON data
    mock_data = {
        "order": ["order", "buy"],
    }
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=mock_data)

    recognizer = IntentRecognizer()

    # Test case insensitivity
    assert recognizer.recognize_intent("I want to ORDER something") == "order"
    assert recognizer.recognize_intent("BUY now") == "order"


def test_recognize_intent_with_empty_database(mocker):
    # Mock an empty JSON file
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value={})

    recognizer = IntentRecognizer()

    # All queries should return 'unknown'
    assert recognizer.recognize_intent("order") == "unknown"
    assert recognizer.recognize_intent("refund") == "unknown"