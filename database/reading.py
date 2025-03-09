import sqlite3
from pprint import pprint

from .create import cursor, conn
from .classes import Recipes, Products, Categories, Fridge
from collections import defaultdict


def reading_recipes() -> list[Recipes]:
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT recipes.id, recipes.name, recipes.description,
               products.id, products.name, recipes_products.amount, products.type,
               categories.id, categories.name
        FROM recipes
        LEFT JOIN recipes_products ON recipes.id = recipes_products.recipes_id
        LEFT JOIN products ON products.id = recipes_products.products_id
        LEFT JOIN categories_products ON products.id = categories_products.products_id
        LEFT JOIN categories ON categories.id = categories_products.categories_id;
    """)
    rows = cursor.fetchall()
    recipes_dict = defaultdict(lambda: {"name": None,
                                        "description": None,
                                        "products": defaultdict(lambda: {"name": None,
                                                                         "amount": None,
                                                                         "product_type": None,
                                                                         'categories': defaultdict(
                                                                             lambda: {"name": None})})})

    for res_id, name, description, product_id, product_name, amount, product_type, category_id, category_name in rows:
        if recipes_dict[res_id]['name'] is None:
            recipes_dict[res_id]['name'] = name
            recipes_dict[res_id]['description'] = description
        if product_id is not None:
            if recipes_dict[res_id]['products'][product_id]['name'] is None:
                recipes_dict[res_id]['products'][product_id]['name'] = product_name
                recipes_dict[res_id]['products'][product_id]['amount'] = amount
                recipes_dict[res_id]['products'][product_id]['product_type'] = product_type
        if category_id is not None:
            if recipes_dict[res_id]['products'][product_id]['categories'][category_id]['name'] is None:
                recipes_dict[res_id]['products'][product_id]['categories'][category_id]['name'] = category_name

    recipes = [Recipes(id=res_id, name=data['name'], description=data['description'],
                       product_list=[(Products(id=product_id, name=product_data['name'],
                                               product_type=product_data['product_type'],
                                               category_list=[Categories(id=category_id,
                                                                         name=category_data['name'])
                                                              for category_id, category_data in
                                                              product_data['categories'].items()]),
                                      product_data['amount'])
                                     for product_id, product_data in data["products"].items()])
               for res_id, data in recipes_dict.items()]
    conn.close()
    return recipes


def reading_categories() -> list[Categories]:
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
            SELECT categories.id, categories.name
            FROM categories
        """)
    rows = cursor.fetchall()
    categories = [Categories(id=row[0], name=row[1]) for row in rows]
    conn.close()
    return categories


def reading_products() -> list[Products]:
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
            SELECT products.id, products.name, products.type,
                   categories.id, categories.name
            FROM products
            LEFT JOIN categories_products ON products.id = categories_products.products_id
            LEFT JOIN categories ON categories.id = categories_products.categories_id;
        """)
    rows = cursor.fetchall()
    products_dict = defaultdict(lambda: {"name": None, "product_type": None,
                                         'categories': defaultdict(lambda: {"name": None})})
    for product_id, product_name, product_type, category_id, category_name in rows:
        if product_id is not None:
            if products_dict[product_id]['name'] is None:
                products_dict[product_id]['name'] = product_name
                products_dict[product_id]['product_type'] = product_type

        if category_id is not None:
            if products_dict[product_id]['categories'][category_id]['name'] is None:
                products_dict[product_id]['categories'][category_id]['name'] = category_name

    products = [Products(id=product_id, name=product_data['name'],
                         product_type=product_data['product_type'],
                         category_list=[Categories(id=category_id,
                                                   name=category_data['name'])
                                        for category_id, category_data in
                                        product_data['categories'].items()])
                for product_id, product_data in products_dict.items()]
    conn.close()
    return products


if __name__ == '__main__':
    pprint(reading_products())
