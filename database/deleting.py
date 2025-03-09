import sqlite3


# удалить все таблицы
def deleting_tables():
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    all_table_names = [row[0] for row in cursor.fetchall()]
    for table_name in all_table_names:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
    conn.close()


def deleting_rows(table_name, id):
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table_name} WHERE id={id}')
    conn.commit()
    conn.close()


def factory_func(table_name: str):
    def new_func(delete_id):
        deleting_rows(table_name, delete_id)

    return new_func


deleteing_products = factory_func('products')
deleteing_recipes = factory_func('recipes')
deleteing_categories = factory_func('categories')
deleteing_fridge = factory_func('fridge')
