import sqlite3

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
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Usuario_TAB (mail, nombre, contra, avatar) VALUES (?, ?, ?, ?)''', 
                           (usuario.mail, usuario.nombre, usuario.contra, usuario.avatar))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Eliminar un usuario de la base de datos
    def delete_usuario(self, mail):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Usuario_TAB WHERE mail = ?''', 
                            (mail,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Encontrar un usuario por su mail
    def find_usuario_by_id(self, mail):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT mail, nombre, contra, avatar FROM Usuario_TAB WHERE mail = ?''', 
                           (mail,))
            row = cursor.fetchone()
            if row:
                return UsuarioVO(row[0], row[1], row[2], row[3])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    # Añadir un avatar a un usuario
    def add_avatar_to_usuario(self, mail, avatar_id):
        try:
            conn = sqlite3.connect('db/database.db')
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
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Usuario_TAB SET avatar = NULL WHERE mail = ?''', 
                           (mail,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()