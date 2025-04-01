import json

from PirateEase.Utils.response_factory import ResponseFactory
from PirateEase.Utils.singleton import Singleton

"""
OOP Principles
- Encapsulation: InventoryProduct encapsulates all the details of a product while InventoryService hides the inventory 
                 data and logic that operates on it.
- Abstraction: The client interacts with check_availability w/o needing to know how the products are stored or matched.
- Composition: InventoryService is composed of InventoryProduct instances which allows for separation of concerns.
- Inheritance: InventoryService inherits from Singleton

Creational Pattern
- Singleton: Ensures centralized management of inventory and that any changes are reflected across the whole system.

SOLID Principles
- Single Responsibility: Inventory Product only models a product and performs matching on itself.
                         InventoryService only loads and checks inventory.
- Open/Close: Can add more product matching techniques by extension or polymorphism
- Liskov Substitution: Both classes can be subclassed w/o breaking core functionality
- Interface Segregation: Each class exposes only necessary and relevant methods.
"""


class InventoryProduct:
    """
    Represents a product in the inventory with a name, quantity, price, list of synonyms, and list of tags.
    """

    def __init__(self, name: str, quantity: int, price: float, synonyms: list[str], tags: list[str]):
        self.name: str = name
        self.quantity: int = quantity
        self.price: float = price
        self.synonyms: list[str] = synonyms
        self.tags: list[str] = tags

    def item_matches_product(self, item: str) -> bool:
        """
        Determine if a given item description matches this product.
        :param item: Item description.
        :return: True if the name or any synonym of this product is a substring of the item, False otherwise.
        """
        return item in self.name or any(synonym in item for synonym in self.synonyms)


class InventoryService(Singleton):
    """
    Singleton class for managing inventory products.
    """

    def __init__(self):
        """
        If not already initialized, loads the current inventory from a database and stores it as a list.
        """
        if self._initialized:
            return

        with open('Databases/inventory.json', 'r', encoding='utf-8') as f:
            raw_products: list[dict] = json.load(f)
        self.__products: list[InventoryProduct] = [
            InventoryProduct(
                name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
                synonyms=item.get("synonyms", []),
                tags=item.get("tags", [])
            )
            for item in raw_products
        ]

        self._initialized = True

    def get_matching_items(self, item: str) -> InventoryProduct or None:
        """
        Gets the first item that matches the given item description. If no item matches, returns None.
        :param item: Item description to match against.
        :return: InventoryProduct matching description or None.
        """
        for product in self.__products:  # For each product in our database
            if product.item_matches_product(item):  # If the product matches the item description
                return product  # Return it
        else:  # No products matched
            return None

    def check_availability(self, item: str) -> str:
        """
        Checks if the given item is available in the current inventory.
        :param item: Description of the item to check.
        :return: String containing information about the availability of the item.
        """
        # Get the matching product
        product: InventoryProduct = self.get_matching_items(item.lower())
        if product is not None:  # If a matching product was found
            # Get its name, quantity, and price
            name: str = product.name
            quantity: int = product.quantity
            price: float = product.price
            if quantity > 0:  # If the item is in stock
                return ResponseFactory.get_response('product_available').format(item=name.title(), quantity=quantity,
                                                                                price=f'${price:.2f}')
            else:  # Else the item is not in stock
                return ResponseFactory.get_response('not_available').format(item=item.title())
        else:  # Else no matching item was found
            return ResponseFactory.get_response('not_sold').format(item=item.title())
