import sqlite3
from classes.posee import PoseeDAO

DB_PATH = '/app/src/db/database.db'

# VO
####
class CampeonVO:
    def __init__(self, nombre, url_buscador, url_campo, url_recom, coste):
        self.nombre = nombre
        self.url_buscador = url_buscador
        self.url_campo = url_campo
        self.url_recom = url_recom
        self.coste = coste

    def to_dict(self): 
        return { 
            'nombre': self.nombre, 
            'url_buscador': self.url_buscador, 
            'url_campo': self.url_campo, 
            'url_recom': self.url_recom, 
            'coste': self.coste,
            'sinergias' : PoseeDAO().get_sinergias_by_champion_id(self.nombre)
        }


# DAO
#####
class CampeonDAO:
    def save_campeon(self, campeon):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Campeon_TAB (nombre, url_buscador, url_campo, url_recom, coste) 
                VALUES (?, ?, ?)
            ''', (campeon.nombre, campeon.url_buscador, campeon.url_campo, campeon.url_recom, campeon.coste))
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
                SELECT nombre, url_buscador, url_campo, url_recom, coste FROM Campeon_TAB WHERE nombre = ?
            ''', (nombre,))
            row = cursor.fetchone()
            if row:
                return CampeonVO(row[0], row[1], row[2], row[3], row[4])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    def get_all_champions(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Campeon_TAB
            ''')
            rows = cursor.fetchall()
            return [CampeonVO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()
