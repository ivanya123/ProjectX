from dataclasses import dataclass
from typing import Optional


@dataclass
class Recipes:
    id:int = None
    name: str = ''
    description: str = ''
    product_list: list[tuple['Products', float]] = None


@dataclass
class Products:
    id:int = None
    name: str = ''
    product_type: str = ''
    category_list: Optional[list['Categories']] = None

@dataclass
class Categories:
    id:int = None
    name: str = ''

@dataclass
class Fridge:
    id:int = None
    products: 'Products' = None
    amount: float = 0.0