import sqlite3
import csv

DATABASE = '/app/src/db/database.db'  # Fichero de la base de datos
SCHEMA = '/app/src/db/schema.sql'     # Fichero con los CREATE TABLE
DATA_FILE = '/app/src/db/data.csv'    # Fichero con los datos a cargar en la base de datos

def init_db():
    conn = sqlite3.connect(DATABASE)
    with open(SCHEMA, 'r') as f:
        conn.executescript(f.read())
    conn.close()

def populate_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    with open(DATA_FILE, 'r') as f:
        reader = csv.reader(f)
        current_table = None
        columns = None
        for row in reader:
            if not row:
                continue
            if len(row) == 1:
                current_table = row[0]
                columns = None
            elif current_table and not columns:
                columns = row
            else:
                values = [int(value) if value.isdigit() else value for value in row]
                placeholders = ', '.join(['?' for _ in values])
                query = f'INSERT INTO {current_table} ({", ".join(columns)}) VALUES ({placeholders})'
                cursor.execute(query, values)
    
    conn.commit()
    conn.close()


init_db()
populate_db()