import json

from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.QueryHandlers.query_manager import QueryManager
from PirateEase.Services.live_agent_notifier import LiveAgentService
from PirateEase.Utils.intent_recognizer import IntentRecognizer
from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.sentiment_analyzer import SentimentAnalyzer
from PirateEase.Utils.session_manager import SessionManager

"""
OOP Principles
- Encapsulation: Each subsystem (intent recognition, sentiment analysis, session management, etc.) is encapsulated and accessed via private attributes.
- Abstraction: process_query() provides a high-level interface that hides the complexity of processing input, routing to handlers, and generating responses.
- Composition: The ChatBot class is composed of multiple helper objects, delegating responsibilities to specialized components.

Behavioral Pattern
- Chain of Responsibility: Delegates query processing to various handlers based on recognized intent.

Structural Pattern
- Facade: Acts as a facade to coordinate between subsystems like session history, backend services, and handlers.

SOLID Principles
- Single Responsibility: Manages the flow of chatbot interaction logic only—does not handle low-level concerns like file I/O or backend responses directly.
- Open/Closed: Supports new intents or handler behaviors by extending QueryManager or adding new handler classes.
- Liskov Substitution: Uses handler objects and services interchangeably through abstract interfaces.
- Interface Segregation: Depends only on small, well-defined interfaces like QueryHandler.
"""


class ChatBot:
    """
    ChatBot for a business with the ability to generating dynamic responses to user inputted queries.
    """

    def __init__(self):
        self.__query_manager: QueryManager = QueryManager()
        self.__intent_recognizer: IntentRecognizer = IntentRecognizer()
        self.__sentiment_analyzer: SentimentAnalyzer = SentimentAnalyzer()
        self.__session_manager: SessionManager = SessionManager()
        self.__agent_service: LiveAgentService = LiveAgentService()
        with open('Databases/intent_phrases.json', 'r', encoding='utf-8') as f:
            self.__exit_phrases = json.load(f).get('exit')

    def process_query(self, query: str) -> str:
        """
        Processes a query by routing it to specific handlers and returns the response.
        :param query: The query to process.
        :return: Response to the query.
        """
        # Add the query to the history
        self.__session_manager.append_history('User: ' + query)
        # Setup up global variables to be used later
        response: str = ''
        db_response: str = self.__query_manager.get_handler('db').handle(query)
        # If negative sentiment is detected
        if self.__sentiment_analyzer.negative_sentiment_detected(query):
            negative_sentiment_response: str = ResponseFactory.get_response('negative')
            live_agent_connection_response: str = \
            self.__query_manager.get_handler('live_agent').handle(query).split('\n', 1)[1]
            response = negative_sentiment_response + '\n' + live_agent_connection_response
        # Else if the database returned a response
        elif db_response:
            response = db_response
        # Else determine the intent and route it to a handler.
        else:
            intent: str = self.__intent_recognizer.recognize_intent(query)
            handler: QueryHandler = self.__query_manager.get_handler(intent)
            response = handler.handle(query.lower().strip())
        # Add the response to the history and return it
        self.__session_manager.append_history(f'PirateEase: {response}')
        return response

    def should_disconnect(self, response: str) -> bool:
        """
        Determines if the current session should be ended.
        :param response: The response to check.
        :return: True if a live agent connection was initiated or if the user used a farewell phrase, False otherwise.
        """
        return (self.__agent_service.agent_name_in_string(response) or
                any(word in response for word in self.__exit_phrases))
