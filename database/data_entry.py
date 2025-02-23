import sqlite3

conn = sqlite3.connect("cooking.db")
cursor = conn.cursor()

recipes_name = "Иван"
recipes_description = 'лучший'

cursor.execute("INSERT INTO recipes (name, description) VALUES (?, ?)", (recipes_name, recipes_description))
cursor.execute("INSERT INTO products (name, type) VALUES (?, ?)", (recipes_name, recipes_description))
cursor.execute("INSERT INTO recipes_products (recipes_id, products_id, amount) VALUES (?, ?, ?)", (8, 2, 20))
cursor.execute("INSERT INTO fridge (products_id, amount) VALUES (?, ?)", (1, 20))

conn.commit()


# recipes
# products
# description
# categories fridge

conn.close()