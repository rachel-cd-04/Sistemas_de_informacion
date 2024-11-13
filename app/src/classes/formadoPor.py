import sqlite3
from classes.campeon import CampeonDAO, CampeonVO

DB_PATH = '/app/src/db/database.db'

# VO
####
class FormadoPorVO:
    def __init__(self, usuario, composicion, campeon):
        self.usuario = usuario
        self.composicion = composicion
        self.campeon = campeon


# DAO
#####
class FormadoPorDAO:
    # Añadir un campeon a una composicion
    def add_campeon_to_composicion(self, formadoPor):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Formada_por_TAB (usuario, composicion, campeon) VALUES (?, ?, ?)''', 
                           (formadoPor.usuario, formadoPor.composicion, formadoPor.campeon))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Quitar un campeon de una composicion
    def remove_campeon_from_composicion(self, usuario, composicion, campeon):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Formada_por_TAB WHERE usuario = ? AND composicion = ? AND campeon = ?''', 
                           (usuario, composicion, campeon))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Encontrar la realcion entre campeon y cmposicion por su id
    def find_formada_por_by_id(self, usuario, composicion, campeon):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT usuario, composicion, campeon FROM Formada_por_TAB WHERE usuario = ? AND composicion = ? AND campeon = ?''', 
                           (usuario, composicion, campeon))
            row = cursor.fetchone()
            if row:
                return FormadoPorVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()



    # Devuelve todos los campeones de una composicion
    def get_champions_by_composicion_id(self, usuario, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT campeon FROM Formada_por_TAB WHERE usuario = ? AND composicion = ?''', 
                           (usuario, composicion))
            campeones = []
            for row in cursor:
                campeon_nombre = row[0]  # Asegúrate de que el índice es correcto
                campeon = CampeonDAO().find_campeon_by_id(campeon_nombre)
                if campeon:
                    campeones.append(campeon)
        
            return campeones
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()