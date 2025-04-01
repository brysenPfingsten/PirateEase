from unittest.mock import mock_open
from PirateEase.Utils.sentiment_analyzer import SentimentAnalyzer


def test_negative_sentiment_detected_with_matching_phrase(mocker):
    # Mock the JSON data
    mock_data = ["angry", "unhappy", "frustrated"]
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=mock_data)

    analyzer = SentimentAnalyzer()

    # Test matching phrases
    assert analyzer.negative_sentiment_detected("I am angry")
    assert analyzer.negative_sentiment_detected("This makes me unhappy")
    assert analyzer.negative_sentiment_detected("I'm frustrated with this")


def test_negative_sentiment_detected_with_no_match(mocker):
    # Mock the JSON data
    mock_data = ["angry", "unhappy", "frustrated"]
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=mock_data)

    analyzer = SentimentAnalyzer()

    # Test non-matching phrases
    assert not analyzer.negative_sentiment_detected("I am happy")
    assert not analyzer.negative_sentiment_detected("This is great")
    assert not analyzer.negative_sentiment_detected("")


def test_negative_sentiment_detected_case_insensitive(mocker):
    # Mock the JSON data
    mock_data = ["angry", "unhappy", "frustrated"]
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=mock_data)

    analyzer = SentimentAnalyzer()

    # Test case insensitivity
    assert analyzer.negative_sentiment_detected("I am ANGRY")
    assert analyzer.negative_sentiment_detected("This makes me UNHAPPY")


def test_negative_sentiment_detected_with_empty_database(mocker):
    # Mock an empty JSON file
    mocker.patch("builtins.open", mock_open())
    mocker.patch("json.load", return_value=[])

    analyzer = SentimentAnalyzer()

    assert not analyzer.negative_sentiment_detected("I am angry")
    assert not analyzer.negative_sentiment_detected("This is terrible")