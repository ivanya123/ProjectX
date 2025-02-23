import sqlite3
from typing import Any

conn = sqlite3.connect("cooking.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master "
               "WHERE type='table' AND name NOT LIKE 'sqlite_%'")
all_table_names = [row[0] for row in cursor.fetchall()]


# recipes
# products
# recipes_products

def reading(table_names: list[str]) -> list[tuple[[str]]]:
    for table_name in table_names:
        try:
            cursor.execute(f'SELECT * FROM {table_name}')
            columns = [desc[0] for desc in cursor.description]
            print(table_name)
            print(columns)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.OperationalError:
            print(f'Нет таблицы {table_name}')


# можно читать все таблицы, несколько или только одну
# reading(['fridge'])
reading(all_table_names)

conn.close()
