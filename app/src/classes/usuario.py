import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class UsuarioVO:
    def __init__(self, mail, nombre, contra, avatar):
        self.mail = mail
        self.nombre = nombre
        self.contra = contra
        self.avatar = avatar

# DAO
#####
class UsuarioDAO:
    # Registrar un nuevo usuario en la base de datos
    def save_usuario(self, usuario):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            sql_query = '''INSERT INTO Usuario_TAB (mail, nombre, contra, avatar) VALUES (?, ?, ?, ?)'''
            cursor.execute(sql_query, (usuario.mail, usuario.nombre, usuario.contra, usuario.avatar))
            conn.commit()
            return usuario
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    # Eliminar un usuario de la base de datos
    def delete_usuario(self, mail):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Usuario_TAB WHERE mail = ?''', 
                            (mail,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Encontrar un usuario por su mail
    def find_usuario_by_id_pssw(self, mail, password):
        conn = None
        try:
            mail = mail.strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            sql_query = '''SELECT mail, nombre, contra, avatar FROM Usuario_TAB WHERE mail = ? AND contra = ?'''
            cursor.execute(sql_query, (mail, password))
            row = cursor.fetchone()
            if row:
                return UsuarioVO(row[0], row[1], row[2], row[3])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # Añadir un avatar a un usuario
    def add_avatar_to_usuario(self, mail, avatar_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''UPDATE Usuario_TAB SET avatar = ? WHERE mail = ?''', 
                           (avatar_id, mail))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Quitar un avatar de un usuario
    def remove_avatar_from_usuario(self, mail):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''UPDATE Usuario_TAB SET avatar = NULL WHERE mail = ?''', 
                           (mail,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()


    # Obtener todos los usuarios
    def get_all_users(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Usuario_TAB ''')
            rows = cursor.fetchall()
            return [UsuarioVO(row[0], row[1], row[2], row[3]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()

    """
    def check_password_hash(self, mail, contra):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT contra FROM Usuario_TAB WHERE mail = ?''', 
                           (mail,))
            row = cursor.fetchone()
            if row:
                return row[0] == contra
            return False
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            conn.close()
    """
