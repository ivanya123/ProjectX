import sqlite3

conn = sqlite3.connect("cooking.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master "
               "WHERE type='table' AND name NOT LIKE 'sqlite_%'")
all_table_names = [row[0] for row in cursor.fetchall()]
def deleting_tables (table_names):
    for table_name in table_names:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

# можно удалить все таблицы, несколько или только одну
#deleting_tables(['products'])
#deleting_tables(all_table_names)

def deleting_rows (table_name, id):
    cursor.execute(f'DELETE FROM {table_name} WHERE id={id}')
    conn.commit()

#удаляем строку в таблице по id
#deleting_rows('recipes', 3)

conn.close()