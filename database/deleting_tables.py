import sqlite3

conn = sqlite3.connect("cooking.db")
cursor = conn.cursor()

table_name = 'products'
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

conn.commit()
conn.close()