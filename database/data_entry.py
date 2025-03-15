import sqlite3
from classes import Recipes, Products, Categories, Fridge


def add_in_recipes(recipes: Recipes):
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO recipes (name, description) VALUES (?, ?)", (recipes.name, recipes.description))
        recipes_id = cursor.lastrowid
        add_in_recipes_products(recipes_id, recipes.product_list, cursor, conn)
    except sqlite3.OperationalError as e:
        print(f'Нет таблицы recipes {e}')
    finally:
        conn.close()


def add_in_recipes_products(recipes_id: int, product_list: list[tuple['Products', float]], cursor, conn):
    for row in product_list:
        cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)",
                       (recipes_id, row[0].id, row[1]))
    conn.commit()


def add_in_products(products: Products):
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, type) VALUES (?, ?)", (products.name, products.product_type))
        products.id = cursor.lastrowid
        if products.category_list:
            for row in products.category_list:
                cursor.execute("INSERT INTO categories_products (categories_id, products_id) VALUES (?, ?)",
                               (row.id, products.id))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы products или categories_products')
    finally:
        conn.close()


def add_in_categories(categories: Categories):
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (categories.name,))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы categories')
    finally:
        conn.close()


def add_in_fridge(fridge: Fridge):
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO fridge (products_id, amount) VALUES (?, ?)", (fridge.products.id, fridge.amount))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы fridge')


# fridge = Fridge(products=Products(id=2), amount = 0.1)
# add_in_fridge(fridge)

if __name__ == '__main__':
    pass
