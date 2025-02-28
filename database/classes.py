from dataclasses import dataclass

@dataclass
class Recipes:
    id=None
    name: str
    description: str

@dataclass
class Products:
    id=None
    name: str
    product_type: str
    category_id: int

@dataclass
class Categories:
    id=None
    name: str

@dataclass
class Fridge:
    id=None
    products_id: int
    amount: float