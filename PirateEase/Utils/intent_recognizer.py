import json

"""
OOP Principles:
- Encapsulation: The internal dictionary of intents is private and only accessed through method calls.
- Abstraction: recognize_intent abstracts the complexity of how it is mapping the query to an intent.

SOLID Principles:
- Single Responsibility: This class has just one job which is to map queries to an intent.
- Interface Segregation: Only exposes what is needed, namely recognize_intent
"""


class IntentRecognizer:
    """
    Class for recognizing intents in user inputting queries.
    """

    def __init__(self):
        """
        Loads a database that contains various words and phrases associated with a certain intent.
        """
        with open('Databases/intent_phrases.json', 'r', encoding='utf-8') as f:
            self.__intent_phrases: dict[str, str] = json.load(f)

    def recognize_intent(self, query: str) -> str:
        """
        Recognizes intent from the given query based on the mappings from the database.
        :param query: The user-inputted query to match an intent to.
        :return: The intent category or unknown if there were no matches.
        """
        for category, phrase in self.__intent_phrases.items():
            # If any phrase in a substring of the query
            if any(phrase in query.lower() for phrase in phrase):
                return category

        # Fallback if nothing matched
        return 'unknown'
