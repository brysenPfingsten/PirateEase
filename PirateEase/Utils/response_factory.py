import json, random
from pathlib import Path

"""
OOP Principles
- Encapsulation: Encapsulates the logic of fetching and returning responses from a JSON file
- Abstraction: Provides a simple interface get_response that does not reveal the way the response is retrieved.

Creational Pattern
- Factory: Centralizes response creation logic which keeps response logic in one place making updates, upgrades,
           and management easier.
           
SOLID Principles
- Single Responsibility: Has one job which is to create responses based on a category.
- Liskov Substitution Principle: A subclass could override get_response w/o breaking expectations.
- Interface Segregation: Provides a single-method interface w/o unnecessary dependencies.
"""


class ResponseFactory:
    """
    Factory for generating random responses based on the given category."
    """
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    responses_path = os.path.join(current_dir, '..', 'Databases', 'responses.json')

    with open(responses_path, 'r', encoding='utf-8') as f:
        responses: dict[str, list[str]] = json.load(f)


    @classmethod
    def get_response(cls, category: str) -> str:
        """
        Returns a random response for the given category.
        :param category: The category of response you want.
        :return: Random response for the given category.
        """
        return random.choice(cls.responses[category])
