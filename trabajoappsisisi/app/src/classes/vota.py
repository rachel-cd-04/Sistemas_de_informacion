import sqlite3

# VO
####
class VotaVO:
    def __init__(self, usuarioVotante, usuarioVotado, composicion):
        self.usuarioVotante = usuarioVotante
        self.usuarioVotado = usuarioVotado
        self.composicion = composicion

# DAO
#####
class VotaDAO:
    # Crear un nuevo voto en la base de datos
    def save_vota(self, vota):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Vota_TAB (usuarioVotante, usuarioVotado, composicion) VALUES (?, ?, ?)''', 
                           (vota.usuarioVotante, vota.usuarioVotado, vota.composicion))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Eliminar un voto de la base de datos
    def delete_vota(self, usuarioVotante, usuarioVotado, composicion):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Vota_TAB WHERE usuarioVotante = ? AND usuarioVotado = ? AND composicion = ?''', 
                           (usuarioVotante, usuarioVotado, composicion))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Encontrar un voto por su id
    def find_vota_by_id(self, usuarioVotante, usuarioVotado, composicion):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT usuarioVotante, usuarioVotado, composicion FROM Vota_TAB WHERE usuarioVotante = ? AND usuarioVotado = ? AND composicion = ?''', 
                           (usuarioVotante, usuarioVotado, composicion))
            row = cursor.fetchone()
            if row:
                return VotaVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()