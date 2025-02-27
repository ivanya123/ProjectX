import sqlite3
from create import cursor, conn

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

def add_in_fridge(products_id: str, amount: float):
    try:
        cursor.execute("INSERT INTO fridge (products_id, amount) VALUES (?, ?)", (products_id, amount))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы fridge')

def add_in_recipes(name: str, description: str, product_list: list[tuple]):
    try:
        cursor.execute("INSERT INTO recipes (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        recipes_id = cursor.lastrowid
        add_in_recipes_products(recipes_id, product_list)
    except sqlite3.OperationalError:
        print('Нет таблицы recipes')

def add_in_recipes_products(recipes_id: int, product_list:list[tuple]):
    for row in product_list:
        cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)",
                       (recipes_id, row[0], row[1]))
        conn.commit()

def add_in_products(name: str, product_type: str, categories_id: int):
    try:
        cursor.execute("INSERT INTO products (name, type) VALUES (?, ?)", (name, product_type))
        conn.commit()
        products_id = cursor.lastrowid
        cursor.execute("INSERT INTO categories_products (categories_id, products_id) VALUES (?, ?)", (categories_id, products_id))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы products или categories_products')

def add_in_categories(name: str):
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы categories')


#add_in_products('курица', 'кг', 2)
#add_in_categories('молочное')
#add_in_fridge(2,10)
#adding('recipes', '1', '1')
add_in_recipes_products(2, [(8, 20)])

# recipes
# products
# recipes_products
# categories
# fridge
# categories_products
