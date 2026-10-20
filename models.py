# ByteBites Data Models
# Customer: Stores customer information and purchase history.
# Receipt: Represents a transaction and its selected items and total.
# Menu: Manages the collection of available items.
# Item: Stores an item's name, price, category, and popularity rating.


class Customer:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.purchase_history: list["Receipt"] = []

    # Record a completed receipt in this customer's history.
    def add_purchase(self, receipt: "Receipt") -> None:
        self.purchase_history.append(receipt)

    # Return a copy so callers can't change the history directly.
    def get_purchase_history(self) -> list["Receipt"]:
        return list(self.purchase_history)

    # A customer counts as a real user once they have at least one purchase.
    def is_verified(self) -> bool:
        return len(self.purchase_history) > 0


class Receipt:
    def __init__(self) -> None:
        self.items: list["Item"] = []

    # Add one selected item; picking the same item twice means a quantity of two.
    def add_item(self, item: "Item") -> None:
        self.items.append(item)

    def get_items(self) -> list["Item"]:
        return list(self.items)

    # Sum the prices of all selected items, rounded to cents.
    def compute_total(self) -> float:
        return round(sum((item.price for item in self.items), 0.0), 2)


class Menu:
    def __init__(self) -> None:
        self.items: list["Item"] = []

    def add_item(self, item: "Item") -> None:
        self.items.append(item)

    def get_all_items(self) -> list["Item"]:
        return list(self.items)

    # Return the items whose category matches exactly, e.g. "Drinks".
    def filter_by_category(self, category: str) -> list["Item"]:
        return [item for item in self.items if item.category == category]

    # Return a new list of items, most popular first. The menu itself is unchanged.
    def sort_by_popularity(self) -> list["Item"]:
        return sorted(self.items, key=lambda item: item.popularity_rating, reverse=True)


class Item:
    def __init__(self, name: str, price: float, category: str, popularity_rating: float) -> None:
        self.name: str = name
        self.price: float = price
        self.category: str = category
        self.popularity_rating: float = popularity_rating


if __name__ == "__main__":
    # Manual test scenario
    burger = Item("Spicy Burger", 8.99, "Entrees", 4.7)
    soda = Item("Large Soda", 1.99, "Drinks", 4.2)
    tea = Item("Iced Tea", 2.49, "Drinks", 3.8)
    cake = Item("Chocolate Cake", 4.50, "Desserts", 4.9)

    menu = Menu()
    for item in (burger, soda, tea, cake):
        menu.add_item(item)
    print("All items:", [i.name for i in menu.get_all_items()])

    print("Drinks:", [i.name for i in menu.filter_by_category("Drinks")])
    print("Desserts:", [i.name for i in menu.filter_by_category("Desserts")])
    print("Snacks (none):", [i.name for i in menu.filter_by_category("Snacks")])

    print("By popularity:", [(i.name, i.popularity_rating) for i in menu.sort_by_popularity()])
    print("Menu order unchanged:", [i.name for i in menu.get_all_items()])

    customer = Customer("Ana")
    print("Verified before purchase:", customer.is_verified())

    receipt = Receipt()
    print("Empty receipt total:", receipt.compute_total())
    receipt.add_item(burger)
    receipt.add_item(soda)
    receipt.add_item(soda)
    print("Receipt items:", [i.name for i in receipt.get_items()])
    print("Receipt total:", receipt.compute_total())  # 8.99 + 1.99 + 1.99 = 12.97

    customer.add_purchase(receipt)
    print("Purchases:", len(customer.get_purchase_history()))
    print("Verified after purchase:", customer.is_verified())
