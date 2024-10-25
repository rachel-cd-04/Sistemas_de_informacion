import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class CampeonVO:
    def __init__(self, nombre, url_, coste):
        self.nombre = nombre
        self.url_ = url_
        self.coste = coste


# DAO
#####
class CampeonDAO:
    def save_campeon(self, campeon):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Campeon_TAB (nombre, url_, coste) 
                VALUES (?, ?, ?)
            ''', (campeon.nombre, campeon.url_, campeon.coste))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def delete_campeon(self, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM Campeon_TAB WHERE nombre = ?
            ''', (nombre,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def find_campeon_by_id(self, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT nombre, url_, coste FROM Campeon_TAB WHERE nombre = ?
            ''', (nombre,))
            row = cursor.fetchone()
            if row:
                return CampeonVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()
