import sqlite3


def new_bd():
    conn = sqlite3.connect("cooking.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes_products (
                recipes_id INT,
                products_id INT,
                amount REAL NOT NULL,
                PRIMARY KEY (recipes_id, products_id),
                FOREIGN KEY (recipes_id) REFERENCES recipes(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories_products (
                categories_id INT,
                products_id INT,
                PRIMARY KEY (categories_id, products_id),
                FOREIGN KEY (categories_id) REFERENCES categories(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS fridge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                products_id INT NOT NULL,
                amount INT NOT NULL,
                FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    new_bd()
