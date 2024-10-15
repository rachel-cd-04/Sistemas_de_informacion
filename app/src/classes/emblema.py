import sqlite3

# VO
####
class EmblemaVO:
    def __init__(self, nombre, url_, sinergia):
        self.nombre = nombre
        self.url_ = url_
        self.sinergia = sinergia

# DAO
#####
class EmblemaDAO:
    #Encontrar emblema por su nombre
    def find_emblema_by_id(self, nombre):
        try:
            conn = sqlite3.connect('db/database.db')
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