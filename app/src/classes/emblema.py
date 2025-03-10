import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class EmblemaVO:
    def __init__(self, nombre, url_, sinergia):
        self.nombre = nombre
        self.url_ = url_
        self.sinergia = sinergia

    # Método to_dict 
    def to_dict(self): 
        return { 
            "nombre": self.nombre, 
            "url_": self.url_, 
            "sinergia": self.sinergia 
        }

# DAO
#####
class EmblemaDAO:
    #Encontrar emblema por su nombre
    def find_emblema_by_id(self, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT nombre, url_, sinergia FROM Emblema_TAB WHERE nombre = ?''', 
                            (nombre,))
            row = cursor.fetchone()
            if row:
                return EmblemaVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    # Obtener todos los emblemas
    def get_all_emblems(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT nombre, url_, sinergia FROM Emblema_TAB''')
            rows = cursor.fetchall()
            emblems = [EmblemaVO(row[0], row[1], row[2]) for row in rows]
            return emblems
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()
