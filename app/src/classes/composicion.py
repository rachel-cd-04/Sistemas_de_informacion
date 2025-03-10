import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class ComposicionVO:
    def __init__(self, usuario, nombre, dificultad, publicado, descr):
        self.usuario = usuario
        self.nombre = nombre
        self.dificultad = dificultad
        self.publicado = publicado
        self.descr = descr

# DAO
#####
class ComposicionDAO:
    # Guardar una nueva composicion en la base de datos
    def save_composicion(self, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Composicion_TAB (usuario, nombre, dificultad, publicado, descr) VALUES (?, ?, ?, ?, ?)''', 
                           (composicion.usuario, composicion.nombre, composicion.dificultad, composicion.publicado, composicion.descr))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Eliminar una composicion de la base de datos
    def delete_composicion(self, usuario, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Composicion_TAB WHERE usuario = ? AND nombre = ?''', 
                           (usuario, nombre))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Encontrar una composicion por su id
    def find_composicion_by_id(self, usuario, nombre):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT usuario, nombre, dificultad, publicado, descr FROM Composicion_TAB WHERE usuario = ? AND nombre = ?''', 
                           (usuario, nombre))
            row = cursor.fetchone()
            if row:
                return ComposicionVO(row[0], row[1], row[2], row[3], row[4])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    # Modificar una composicion existente en la base de datos
    def update_composicion(self, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''UPDATE Composicion_TAB SET dificultad = ?, publicado = ?, descr = ? WHERE usuario = ? AND nombre = ?''', 
                           (composicion.dificultad, composicion.publicado, composicion.descr, composicion.usuario, composicion.nombre))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Publicar o despublicar una composicion
    def set_publicado(self, usuario, nombre, publicado):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Composicion_TAB 
                SET publicado = ? 
                WHERE usuario = ? AND nombre = ?
            ''', (publicado, usuario, nombre))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Obtener todas las composiciones de un usuario
    def get_composiciones_by_usuario_id(self, usuario_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Composicion_TAB WHERE usuario = ?''', 
                           (usuario_id,))
            rows = cursor.fetchall()
            return [ComposicionVO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()

    # Obtener todas las composiciones publicadas
    def get_all_public_composiciones(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Composicion_TAB WHERE publicado = "Y"''')
            rows = cursor.fetchall()
            return [ComposicionVO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()

    
     # Obtener todas las composiciones publicadas
    def get_all_composiciones(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Composicion_TAB ''')
            rows = cursor.fetchall()
            return [ComposicionVO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()