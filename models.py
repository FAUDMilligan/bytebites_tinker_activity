# ByteBites Data Models
# Customers: Stores customer information and purchase history.
# Receipt: Represents a transaction and its selected items and total.
# Menu: Manages the collection of available items.
# Item: Stores an item's name, price, category, and popularity rating.  






class Customer:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.purchase_history: list["Receipt"] = []

    def add_purchase(self, receipt: "Receipt") -> None:
        pass

    def get_purchase_history(self) -> list["Receipt"]:
        pass

    def is_verified(self) -> bool:
        pass


class Receipt:
    def __init__(self) -> None:
        self.items: list["Item"] = []

    def add_item(self, item: "Item") -> None:
        pass

    def get_items(self) -> list["Item"]:
        pass

    def compute_total(self) -> float:
        pass


class Menu:
    def __init__(self) -> None:
        self.items: list["Item"] = []

    def add_item(self, item: "Item") -> None:
        pass

    def get_all_items(self) -> list["Item"]:
        pass

    def filter_by_category(self, category: str) -> list["Item"]:
        pass


class Item:
    def __init__(self, name: str, price: float, category: str, popularity_rating: float) -> None:
        self.name: str = name
        self.price: float = price
        self.category: str = category
        self.popularity_rating: float = popularity_rating