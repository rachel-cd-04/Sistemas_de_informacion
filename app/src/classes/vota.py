import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class VotaVO:
    def __init__(self, usuarioVotante, usuarioVotado, composicion, voto):
        self.usuarioVotante = usuarioVotante
        self.usuarioVotado = usuarioVotado
        self.composicion = composicion
        self.voto = voto

# DAO
#####
class VotaDAO:
    # Crear un nuevo voto en la base de datos
    def save_vota(self, vota):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Vota_TAB (usuarioVotante, usuarioVotado, composicion) VALUES (?, ?, ?, ?)''', 
                           (vota.usuarioVotante, vota.usuarioVotado, vota.composicion, vota.voto))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Eliminar un voto de la base de datos
    def delete_vota(self, usuarioVotante, usuarioVotado, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
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
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT usuarioVotante, usuarioVotado, composicion FROM Vota_TAB WHERE usuarioVotante = ? AND usuarioVotado = ? AND composicion = ?''', 
                           (usuarioVotante, usuarioVotado, composicion))
            row = cursor.fetchone()
            if row:
                return VotaVO(row[0], row[1], row[2], row[3])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()


    # Encontrar un voto por su id
    def find_votes_to_comp(self, usuarioVotado, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            #cursor.execute('''SELECT COUNT(*) FROM Vota_TAB WHERE usuarioVotado = ? AND composicion = ?''', 
            #               (usuarioVotado, composicion))
            #return cursor.fetchone()[0]
            cursor.execute('''SELECT usuarioVotante, usuarioVotado, composicion FROM Vota_TAB WHERE WHERE usuarioVotado = ? AND composicion = ?''', 
                           (usuarioVotado, composicion))
            row = cursor.fetchone()
            if row:
                return VotaVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return 0
        finally:
            conn.close()