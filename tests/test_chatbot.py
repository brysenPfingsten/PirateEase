import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from PirateEase.chatbot import ChatBot


@pytest.fixture
def mock_dependencies():
    exit_data = json.dumps({"exit": ["goodbye", "bye", "see you"]})
    m = mock_open(read_data=exit_data)

    with patch("builtins.open", m):
        yield


@pytest.fixture
def bot(mock_dependencies):
    # Patch all components used internally
    with patch("PirateEase.chatbot.QueryManager"), \
            patch("PirateEase.chatbot.IntentRecognizer"), \
            patch("PirateEase.chatbot.SentimentAnalyzer"), \
            patch("PirateEase.chatbot.SessionManager"), \
            patch("PirateEase.chatbot.LiveAgentService"):


        return ChatBot()


def test_process_query_negative_sentiment(bot):
    with patch.object(bot._ChatBot__sentiment_analyzer, "negative_sentiment_detected", return_value=True), \
            patch("PirateEase.chatbot.ResponseFactory.get_response", return_value="I'm sorry to hear that."), \
            patch.object(bot._ChatBot__query_manager, "get_handler") as mock_get_handler:
        # Simulate live agent handler returning a response
        mock_handler = MagicMock()
        mock_handler.handle.return_value = "PirateEase: A live agent will help you.\nConnecting you to Jack"
        mock_get_handler.return_value = mock_handler

        result = bot.process_query("This is terrible.")

        assert "I'm sorry to hear that." in result
        assert "Connecting you to Jack" in result


def test_process_query_from_database(bot):
    with patch.object(bot._ChatBot__sentiment_analyzer, "negative_sentiment_detected", return_value=False), \
            patch.object(bot._ChatBot__query_manager.get_handler("db"), "handle", return_value="Yes, we do sell that!"):
        result = bot.process_query("Do you sell swords?")
        assert result == "Yes, we do sell that!"


def test_process_query_with_intent_routing(bot):
    # Sentiment is not negative
    with patch.object(bot._ChatBot__sentiment_analyzer, "negative_sentiment_detected", return_value=False), \
            patch.object(bot._ChatBot__intent_recognizer, "recognize_intent", return_value="refund"), \
            patch.object(bot._ChatBot__query_manager, "get_handler") as mock_get_handler:

        # First call: get_handler("db") should return a mock that returns an empty string
        db_handler_mock = MagicMock()
        db_handler_mock.handle.return_value = ""

        # Second call: get_handler("refund") should return another mock
        refund_handler_mock = MagicMock()
        refund_handler_mock.handle.return_value = "Refund submitted successfully."

        # Configure the mock to return different handlers based on input
        def side_effect(intent):
            if intent == "db":
                return db_handler_mock
            elif intent == "refund":
                return refund_handler_mock
            else:
                raise ValueError("Unexpected handler")

        mock_get_handler.side_effect = side_effect

        # Run the function
        result = bot.process_query("I want a refund.")

        assert result == "Refund submitted successfully."
        refund_handler_mock.handle.assert_called_once()


def test_should_disconnect_on_agent_name(bot):
    with patch.object(bot._ChatBot__agent_service, "agent_name_in_string", return_value=True):
        result = bot.should_disconnect("Connecting you to Anne Bonny...")
        assert result is True


def test_should_disconnect_on_exit_phrase(bot):
    with patch.object(bot._ChatBot__agent_service, "agent_name_in_string", return_value=False):
        result = bot.should_disconnect("Thanks, bye!")
        assert result is True


def test_should_not_disconnect(bot):
    with patch.object(bot._ChatBot__agent_service, "agent_name_in_string", return_value=False):
        result = bot.should_disconnect("Tell me about cutlasses.")
        assert result is False
