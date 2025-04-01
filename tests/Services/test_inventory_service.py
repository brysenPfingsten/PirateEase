import pytest
from unittest.mock import patch, mock_open
import json
from PirateEase.Services.inventory_service import InventoryService, InventoryProduct

# Test data for inventory.json
TEST_INVENTORY = [
    {
        "name": "gold coin",
        "quantity": 10,
        "price": 1.99,
        "synonyms": ["doubloon"],
        "tags": ["currency"]
    },
    {
        "name": "silver cup",
        "quantity": 0,
        "price": 29.99,
        "synonyms": ["goblet"],
        "tags": ["tableware"]
    }
]


@pytest.fixture
def mock_inventory_file():
    with patch("builtins.open", mock_open(read_data=json.dumps(TEST_INVENTORY))):
        yield


@pytest.fixture
def mock_response_factory():
    """Fixture to mock ResponseFactory"""
    with patch("PirateEase.Services.inventory_service.ResponseFactory") as mock:
        mock.get_response.side_effect = lambda x: {
            'product_available': "We have {quantity} {item} available for {price}",
            'not_available': "Sorry, {item} is currently out of stock",
            'not_sold': "We don't sell {item}"
        }.get(x, "")
        yield mock


def test_inventory_product_matching():
    """Test InventoryProduct matching functionality"""
    product = InventoryProduct(
        name="gold coin",
        quantity=10,
        price=1.99,
        synonyms=["doubloon"],
        tags=["currency"]
    )

    # Test exact name match
    assert product.item_matches_product("gold coin")

    # Test synonym match
    assert product.item_matches_product("gold doubloon")

    # Test partial match
    assert product.item_matches_product("coin")

    # Test no match
    assert not product.item_matches_product("silver")


def test_inventory_service_singleton(mock_inventory_file):
    instance1 = InventoryService()
    instance2 = InventoryService()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)

def test_get_matching_items(mock_inventory_file):
    service = InventoryService()

    # Test exact match
    product = service.get_matching_items("gold coin")
    assert product.name == "gold coin"

    # Test synonym match
    product = service.get_matching_items("doubloon")
    assert product.name == "gold coin"

    # Test no match
    assert service.get_matching_items("diamond") is None


def test_check_availability_in_stock(mock_inventory_file, mock_response_factory):
    service = InventoryService()
    result = service.check_availability("gold coin")
    assert "We have 10 Gold Coin available for $1.99" in result
    mock_response_factory.get_response.assert_called_with('product_available')


def test_check_availability_out_of_stock(mock_inventory_file, mock_response_factory):
    service = InventoryService()
    result = service.check_availability("silver cup")
    assert "Sorry, Silver Cup is currently out of stock" in result
    mock_response_factory.get_response.assert_called_with('not_available')


def test_check_availability_not_sold(mock_inventory_file, mock_response_factory):
    service = InventoryService()
    result = service.check_availability("diamond")
    assert "We don't sell Diamond" in result
    mock_response_factory.get_response.assert_called_with('not_sold')


def test_reset_behavior(mock_inventory_file):
    instance1 = InventoryService()
    InventoryService.reset()
    instance2 = InventoryService()
    assert instance1 is not instance2