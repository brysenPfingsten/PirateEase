import json

from PirateEase.QueryHandlers.abc_handler import QueryHandler

"""
OOP Principles
- Encapsulation: Manages the query-response mapping internally and exposes only the handle() method.
- Abstraction: Consumers don’t need to know how data is stored or matched—only that a response is returned.
- Inheritance: Inherits from QueryHandler, allowing polymorphic behavior in a handler chain.

Behavioral Pattern
- Chain of Responsibility: Acts as one handler in a chain, returning a response for known queries or deferring to others.

SOLID Principles
- Single Responsibility: Handles one thing—looking up and returning predefined responses.
- Open/Closed: Can load new queries via the JSON file or override handle() in a subclass without modifying base logic.
- Liskov Substitution: Can substitute any other QueryHandler without breaking the system.
- Interface Segregation: Only implements the required handle() method from QueryHandler.
"""


class QueryDatabase(QueryHandler):
    """
    QueryHandler for predefined query/responses.
    """
    def __init__(self) -> None:
        super().__init__()
        # Load the DB of predefined query and responses
        with open('Databases/queries.json', 'r', encoding='utf-8') as f:
            self.queries: dict[str, str] = json.load(f)

    def handle(self, query: str)  -> str:
        """
        Matches the given query against a database of predefined queries and returns the result if it exists.
        :param query: The query to match.
        :return: Matching response or empty string.
        """
        response: str = self.queries.get(query.lower())
        if response is not None:
            return response
        else:
            return ''