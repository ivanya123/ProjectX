import sqlite3

conn = sqlite3.connect("cooking.db")
cursor = conn.cursor()


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


def add_in_fridge(product_name: str, amount: float) -> tuple[str, float]:
    pass


# пишешь название таблицы и данные по порядку (то же кол-во, что и столбцов, не считая id (он проставляется автоматом)!)
adding('recipes', '1', '1')

conn.close()

# recipes
# products
# recipes_products
# categories
# fridge
# categories_products
