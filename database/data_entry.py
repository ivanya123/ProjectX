import sqlite3
from create import cursor, conn
from classes import Recipes, Products, Categories, Fridge

def adding(table_name, *values):
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall() if row[1] != 'id']
        result = ", ".join(columns)
        result_val = ", ".join(["?" for _ in columns])
        cursor.execute(f"INSERT INTO {table_name} ({result}) VALUES ({result_val})", values)
        conn.commit()
    except sqlite3.OperationalError:
        print(f'Нет таблицы {table_name}')



def add_in_recipes(recipes: Recipes, product_list: list[tuple]):
    try:
        cursor.execute("INSERT INTO recipes (name, description) VALUES (?, ?)", (recipes.name, recipes.description))
        recipes_id = cursor.lastrowid
        add_in_recipes_products(recipes_id, product_list)
    except sqlite3.OperationalError:
        print('Нет таблицы recipes')

def add_in_recipes_products(recipes_id: int, product_list:list[tuple]):
    for row in product_list:
        cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)",
                       (recipes_id, row[0], row[1]))
        conn.commit()

def add_in_products(products: Products):
    try:
        cursor.execute("INSERT INTO products (name, type) VALUES (?, ?)", (products.name, products.product_type))
        products.id = cursor.lastrowid
        cursor.execute("INSERT INTO categories_products (categories_id, products_id) VALUES (?, ?)", (products.category_id, products.id))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы products или categories_products')

# new_product = Products (name="Алексеctcй", product_type="alex@example.com", category_id = 1)
# add_in_products(new_product)

def add_in_categories(categories: Categories):
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (categories.name,))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы categories')

def add_in_fridge(fridge: Fridge):
    try:
        cursor.execute("INSERT INTO fridge (products_id, amount) VALUES (?, ?)", (fridge.products_id, fridge.amount))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы fridge')


#add_in_products('курица', 'кг', 2)
#add_in_categories('молочное')
#add_in_fridge(2,10)
#adding('recipes', '1', '1')
#add_in_recipes_products(2, [(8, 20)])

# recipes
# products
# recipes_products
# categories
# fridge
# categories_products
