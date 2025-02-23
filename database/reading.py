import sqlite3

conn = sqlite3.connect("cooking.db")
cursor = conn.cursor()

# recipes
# products
# recipes_products

table_name = 'fridge'

try:
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    print(table_name)
    print(columns)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except sqlite3.OperationalError:
    print(f'Нет таблицы {table_name}')

conn.close()