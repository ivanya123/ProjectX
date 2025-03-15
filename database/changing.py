import sqlite3
from classes import Recipes, Products, Categories, Fridge


# def changing_recipes(recipes:Recipes):
#     with sqlite3.connect("cooking.db") as conn:
#         conn.execute("PRAGMA foreign_keys = ON")
#         cursor = conn.cursor()
#
#         cursor.execute("UPDATE recipes "
#                        "SET name = ?,"
#                        "description = ?"
#                        "WHERE id = ?", (recipes.name, recipes.description, recipes.id))
#         if cursor.rowcount > 0:
#             print("OK")
#             list_id_am = [(product.id, amount) for product, amount in recipes.product_list]
#             str_id = ', '.join(str(p_id) for p_id, _ in list_id_am)
#             cursor.execute(f'DELETE FROM recipes_products WHERE recipes_id = {recipes.id} and products_id not in ({str_id})')
#             for product, amount in recipes.product_list:
#                 cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)",
#                                (recipes.id, product.id, amount))
#
#
#                 "INSERT  recipes_products "
#                                "SET products_id =?, amount =?"
#                                "WHERE recipes_id = ?", (product.id, amount, recipes.id))
#                 if cursor.rowcount > 0:
#                     print("product_OK")
#         conn.commit()

# changing_recipes(Recipes(id=1, name='яблоки с рыбой', description = 'папапа', product_list = [(Products(id=2), 10), (Products(id=1), 8)]))


def changing_del_recipes(recipes: Recipes):
    with sqlite3.connect("cooking.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("UPDATE recipes "
                       "SET name = ?,"
                       "description = ?"
                       "WHERE id = ?", (recipes.name, recipes.description, recipes.id))
        if cursor.rowcount > 0:
            print("OK")
        cursor.execute(f'DELETE FROM recipes_products WHERE recipes_id = {recipes.id}')
        for product, amount in recipes.product_list:
            cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)",
                           (recipes.id, product.id, amount))
        conn.commit()

# if __name__ == '__main__':
#     changing_del_recipes(Recipes(id=1, name='яблоки с рыбой', description = 'папапа', product_list = [(Products(id=2), 10), (Products(id=1), 8)]))

def changing_del_products(products: Products):
    with sqlite3.connect("cooking.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("UPDATE products "
                       "SET name = ?,"
                       "type = ?"
                       "WHERE id = ?", (products.name, products.product_type, products.id))
        if cursor.rowcount > 0:
            print("OK")
        cursor.execute(f'DELETE FROM categories_products WHERE products_id = {products.id}')
        for categories in products.category_list:
            cursor.execute("INSERT INTO categories_products (categories_id, products_id) VALUES (?, ?)",
                           (categories.id, products.id))
        conn.commit()

# if __name__ == '__main__':
#     changing_del_products(Products(id=2, name='брокколи', product_type='кг', category_list=[Categories(id=2)]))

def changing_categories(categories: Categories):
    with sqlite3.connect("cooking.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("UPDATE categories "
                       "SET name = ?"
                       "WHERE id = ?", (categories.name, categories.id))
        conn.commit()

def changing_fridge(fridge: Fridge):
    with sqlite3.connect("cooking.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("UPDATE fridge "
                       "SET amount = ?"
                       "WHERE id = ?", (fridge.amount, fridge.id))
        conn.commit()

if __name__ == '__main__':
    changing_categories(Categories(id=3, name='цветное'))
    changing_fridge(Fridge(id=1, amount=10))