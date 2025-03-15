import sqlite3
from classes import Recipes, Products, Categories, Fridge


def changing_recipes(recipes:Recipes):
    with sqlite3.connect("cooking.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("UPDATE recipes "
                       "SET name = ?,"
                       "description = ?"
                       "WHERE id = ?", (recipes.name, recipes.description, recipes.id))
        if cursor.rowcount > 0:
            print("OK")
            for product, amount in recipes.product_list:
                cursor.execute("UPDATE recipes_products "
                               "SET products_id =?, amount =?"
                               "WHERE recipes_id = ?", (product.id, amount, recipes.id))
                if cursor.rowcount > 0:
                    print("product_OK")
        conn.commit()

changing_recipes(Recipes(id=1, name='яблоки с рыбой', description = 'папапа', product_list = [(Products(id=2), 10), (Products(id=1), 8)]))