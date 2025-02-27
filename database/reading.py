import sqlite3
from create import cursor, conn


cursor.execute("SELECT name FROM sqlite_master "
               "WHERE type='table' AND name NOT LIKE 'sqlite_%'")
all_table_names = [row[0] for row in cursor.fetchall()]


# recipes
# products
# recipes_products

def reading(table_name: str) -> list[tuple[[str]]]:
    try:
        cursor.execute(f'SELECT * FROM {table_name}')
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        print(f'Нет таблицы {table_name}')
    return columns, rows

# можно вывести только одну таблицу
print(reading('recipes_products'))

def reading_products():
    try:
        cursor.execute('SELECT * FROM products')
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        print('Нет таблицы products')
    return columns, rows

print(reading_products())

conn.close()
