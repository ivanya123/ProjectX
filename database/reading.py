import sqlite3
from pprint import pprint

from create import cursor, conn
from classes import Recipes, Products, Categories, Fridge
from collections import defaultdict


def reading_recipes():
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
    # columns = [desc[0] for desc in cursor.description] -- если нужно вывести названия колонок
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

    # for res in recipes:
    #     print(res)
    return recipes


if __name__ == '__main__':
    pprint(reading_recipes())
