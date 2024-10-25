import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class SinergiaVO:
    def __init__(self, nombre, unidades_mejora):
        self.nombre = nombre
        self.unidades_mejora = unidades_mejora

# DAO
#####
class SinergiaDAO:
    # Encontrar sinergia por su nombre
    def find_sinergia_by_id(self, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT nombre, unidades_mejora FROM Sinergia_TAB WHERE nombre = ?''', 
                           (nombre,))
            row = cursor.fetchone()
            if row:
                return SinergiaVO(row[0], row[1])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()