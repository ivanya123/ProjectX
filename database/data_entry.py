import sqlite3
from create import cursor, conn
from classes import Recipes, Products, Categories, Fridge

# def adding(table_name, *values):
#     try:
#         cursor.execute(f"PRAGMA table_info({table_name})")
#         columns = [row[1] for row in cursor.fetchall() if row[1] != 'id']
#         result = ", ".join(columns)
#         result_val = ", ".join(["?" for _ in columns])
#         cursor.execute(f"INSERT INTO {table_name} ({result}) VALUES ({result_val})", values)
#         conn.commit()
#     except sqlite3.OperationalError:
#         print(f'Нет таблицы {table_name}')



def add_in_recipes(recipes: Recipes):
    try:
        cursor.execute("INSERT INTO recipes (name, description) VALUES (?, ?)", (recipes.name, recipes.description))
        recipes_id = cursor.lastrowid
        add_in_recipes_products(recipes_id, recipes.product_list)
    except sqlite3.OperationalError:
        print('Нет таблицы recipes')

def add_in_recipes_products(recipes_id: int, product_list: list[tuple['Products', float]]):
    for row in product_list:
        cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)",
                       (recipes_id, row[0].id, row[1]))
        conn.commit()

# add_in_recipes(recipes=Recipes(name='тушеные овощи', description='очень полезно',
#                                product_list=[(Products(id=3, name='овощи', product_type='шт',
#                                                        category_list = [Categories(id=2, name = 'зеленое'), Categories(id=1, name = 'основное')]), 10),
#                                              (Products(id=2, name='зелень', product_type='г',
#                                                        category_list=[Categories(id=2, name = 'зеленое')]), 100)
#                                              ]))

def add_in_products(products: Products):
    try:
        cursor.execute("INSERT INTO products (name, type) VALUES (?, ?)", (products.name, products.product_type))
        products.id = cursor.lastrowid
        for row in products.category_list:
            cursor.execute("INSERT INTO categories_products (categories_id, products_id) VALUES (?, ?)", (row.id, products.id))
            conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы products или categories_products')

# new_product = Products (name="овощи", product_type="шт", category_list = [Categories(id=2, name = 'зеленое'), Categories(id=1, name = 'основное')])
# add_in_products(new_product)

def add_in_categories(categories: Categories):
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (categories.name,))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы categories')

# add_in_categories(Categories(name='жидкость'))

def add_in_fridge(fridge: Fridge):
    try:
        cursor.execute("INSERT INTO fridge (products_id, amount) VALUES (?, ?)", (fridge.products.id, fridge.amount))
        conn.commit()
    except sqlite3.OperationalError:
        print('Нет таблицы fridge')

# add_in_fridge(Fridge(products=Products(id = 2, name="рыба", product_type="кг", category_list = [Categories(id=1, name = 'мясо')]),amount=3.2))