from PirateEase.QueryHandlers.abc_handler import QueryHandler
from PirateEase.Utils.response_factory import ResponseFactory

"""
OOP Principles
- Encapsulation: Encapsulates logic for handling unrecognized queries in a single method and class.
- Abstraction: handle does not reveal how the query is logged or how the response is generated.
- Inheritance: Inherits from QueryHandler allowing for polymorphism.

Behavioral Pattern
- Chain of Responsibility: This is the fallback handler at the end of the chain when no other handler can process a query.
                           This ensures that every question receives a response and makes the system more robust.

SOLID Principles
- Single Responsibility: Only handles unrecognized queries.
- Open/Closed: Can be extended with more advanced ways to handle an unknown query w/o modifying this implementation.
- Liskov Substitution: Can replace QueryHandler anywhere w/o breaking the code.
- Interface Segregation: Only implements the relevant method from QueryHandler.
"""


class DefaultHandler(QueryHandler):
    """
    Class for handling unknown queries.
    """

    def handle(self, query: str) -> str:
        """
        Logs the unknown query and returns a response indicating the query was not understood.
        :param query: The query to be logged.
        :return: Response indicating the query was not understood.
        """
        with open("Databases/unrecognized_queries.txt", "a", encoding='utf-8') as f:
            f.write(query + '\n')
        return ResponseFactory.get_response('default')
