import json

"""
OOP Principles
- Encapsulation: Encapsulates the logic and data for detecting negative sentiments.
- Abstraction: negative_sentiment_detected is a simple interface for checking for negative sentiments w/o
               revealing how it is done.

SOLID Principles
- Single Responsibility: Sole responsibility is to determine if a query has negative sentiment.
- Liskov Substitution: Can be subclassed for more complex analyzer or composed for other types of sentiments.
- Interface Segregation: Provides only one clear method.
"""


class SentimentAnalyzer:
    """
    Detects negative sentiment in user queries.
    """

    def __init__(self):
        """
        Loads a list of phrases with negative or aggressive intent.
        """
        with open('Databases/negative_phrases.json', 'r', encoding='utf-8') as f:
            self.negative_phrases: list[str] = json.load(f)

    def negative_sentiment_detected(self, query: str) -> bool:
        """
        Detects negative sentiment in user queries.
        :param query: The query to detect negative sentiment in.
        :return: True if negative sentiment is detected, False otherwise.
        """
        return any(phrase in query.lower() for phrase in self.negative_phrases)
