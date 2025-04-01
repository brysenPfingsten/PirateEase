from PirateEase.QueryHandlers.abc_handler import QueryHandler

"""
OOP Principles
- Encapsulation: Encapsulates exit-handling logic inside a dedicated class and method.
- Abstraction: Caller doesn't need to know how the exit response is generated or where it comes from.
- Inheritance: Inherits from QueryHandler allowing it to be used polymorphically in a handler chain.

Behavioral Pattern
- Chain of Responsibility: Designed to be part of a chain where it handles exit-specific queries and passes on others (if extended).

SOLID Principles
- Single Responsibility: Only responsible for handling exit-related queries.
- Open/Closed: Can be extended with more logic such as a confirmation prompt without modifying existing code.
- Liskov Substitution: Can replace QueryHandler anywhere without breaking behavior.
- Interface Segregation: Only implements the required handle() method from QueryHandler.
"""


class ExitHandler(QueryHandler):
    """
    QueryHandler that provides farewell responses.
    """

    def handle(self, query: str) -> str:
        """
        Dynamically generates a farewell response.
        :param query: Doesn't matter
        :return: Dynamically generated farewell response
        """
        return self._backend.process_request('exit')
