import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class SinergiaVO:
    def __init__(self, nombre, url_, unidades_mejora):
        self.nombre = nombre
        self.url_ = url_
        self.unidades_mejora = unidades_mejora

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'url_': self.url_,
            'unidades_mejora': self.unidades_mejora
        }

# DAO
#####
class SinergiaDAO:
    # Encontrar sinergia por su nombre
    def find_sinergia_by_id(self, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Sinergia_TAB WHERE nombre = ?''', 
                           (nombre,))
            row = cursor.fetchone()
            if row:
                return SinergiaVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    # Encontrar todas las sinergias
    def get_all_sinergias(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Sinergia_TAB''')
            rows = cursor.fetchall()
            sinergias = []
            for row in rows:
                sinergias.append(SinergiaVO(row[0], row[1], row[2]))
            return sinergias
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()