import sqlite3

conn = sqlite3.connect("cooking.db")
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
        amount INT NOT NULL,
        PRIMARY KEY (recipes_id, products_id),
        FOREIGN KEY (recipes_id) REFERENCES recipes(id) ON DELETE CASCADE,
        FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE
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
        FOREIGN KEY (categories_id) REFERENCES categories(id) ON DELETE CASCADE,
        FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fridge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        products_id INT,
        amount INT NOT NULL,
        FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()