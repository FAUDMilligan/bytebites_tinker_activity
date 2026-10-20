import pytest

from models import Customer, Receipt, Menu, Item


@pytest.fixture
def menu():
    menu = Menu()
    menu.add_item(Item("Spicy Burger", 10.00, "Entrees", 4.7))
    menu.add_item(Item("Large Soda", 5.00, "Drinks", 4.2))
    menu.add_item(Item("Iced Tea", 2.49, "Drinks", 3.8))
    menu.add_item(Item("Chocolate Cake", 4.50, "Desserts", 4.9))
    return menu


# --- Item details ---

# An item should keep the name, price, category, and popularity rating it was given.
def test_item_stores_its_details():
    item = Item("Spicy Burger", 8.99, "Entrees", 4.7)
    assert item.name == "Spicy Burger"
    assert item.price == 8.99
    assert item.category == "Entrees"
    assert item.popularity_rating == 4.7


# --- Receipt totals ---

# A $10 burger and a $5 soda should total $15.
def test_calculate_total_with_multiple_items():
    receipt = Receipt()
    receipt.add_item(Item("Spicy Burger", 10.00, "Entrees", 4.7))
    receipt.add_item(Item("Large Soda", 5.00, "Drinks", 4.2))
    assert receipt.compute_total() == 15.00


# A receipt with nothing added should total $0 instead of crashing.
def test_order_total_is_zero_when_empty():
    total = Receipt().compute_total()
    assert total == 0.0
    assert isinstance(total, float)


# Picking the same item twice should charge for it twice.
def test_total_counts_repeated_items():
    soda = Item("Large Soda", 1.99, "Drinks", 4.2)
    receipt = Receipt()
    receipt.add_item(soda)
    receipt.add_item(soda)
    assert receipt.compute_total() == 3.98


# Prices that don't add up evenly as floats should still total to exact cents.
def test_total_is_rounded_to_cents():
    receipt = Receipt()
    receipt.add_item(Item("Gum", 0.10, "Snacks", 3.0))
    receipt.add_item(Item("Mint", 0.20, "Snacks", 3.0))
    assert receipt.compute_total() == 0.30


# --- Menu filtering ---

# Filtering by "Drinks" should return only the drink items.
def test_filter_by_category_returns_only_matching_items(menu):
    drinks = menu.filter_by_category("Drinks")
    assert [item.name for item in drinks] == ["Large Soda", "Iced Tea"]


# Filtering by a category with no items should return an empty list.
def test_filter_by_category_with_no_matches_returns_empty_list(menu):
    assert menu.filter_by_category("Snacks") == []


# Filtering should not remove anything from the menu.
def test_filter_by_category_does_not_change_menu(menu):
    menu.filter_by_category("Drinks")
    assert len(menu.get_all_items()) == 4


# --- Menu sorting ---

# Sorting by popularity should put the highest-rated item first.
def test_sort_by_popularity_orders_highest_first(menu):
    ratings = [item.popularity_rating for item in menu.sort_by_popularity()]
    assert ratings == [4.9, 4.7, 4.2, 3.8]


# Sorting should return a new list and leave the menu's own order alone.
def test_sort_by_popularity_does_not_change_menu_order(menu):
    menu.sort_by_popularity()
    names = [item.name for item in menu.get_all_items()]
    assert names == ["Spicy Burger", "Large Soda", "Iced Tea", "Chocolate Cake"]


# Sorting an empty menu should return an empty list instead of crashing.
def test_sort_by_popularity_on_empty_menu():
    assert Menu().sort_by_popularity() == []


# --- Customer purchase history ---

# A new customer has no purchases and is not verified.
def test_new_customer_is_not_verified():
    customer = Customer("Ana")
    assert customer.get_purchase_history() == []
    assert customer.is_verified() is False


# A customer with a real purchase is verified and the receipt is in their history.
def test_customer_is_verified_after_purchase():
    customer = Customer("Ana")
    receipt = Receipt()
    receipt.add_item(Item("Large Soda", 1.99, "Drinks", 4.2))
    customer.add_purchase(receipt)
    assert customer.get_purchase_history() == [receipt]
    assert customer.is_verified() is True


# An empty receipt does not count as a real purchase.
def test_empty_receipt_does_not_verify_customer():
    customer = Customer("Ana")
    customer.add_purchase(Receipt())
    assert customer.is_verified() is False
