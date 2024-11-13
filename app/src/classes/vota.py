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
            cursor.execute('''INSERT INTO Vota_TAB (usuarioVotante, usuarioVotado, composicion, voto) VALUES (?, ?, ?, ?)''', 
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
                           (usuarioVotante, usuarioVotado, composicion,))
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
            cursor.execute('''SELECT voto FROM Vota_TAB WHERE usuarioVotante = ? AND usuarioVotado = ? AND composicion = ?''', 
                           (usuarioVotante, usuarioVotado, composicion))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()


    # Encontrar votos positivos a una composición
    def find_good_votes_to_comp(self, usuarioVotado, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(*) FROM Vota_TAB WHERE usuarioVotado = ? AND composicion = ? AND voto = ?''', 
                           (usuarioVotado, composicion, 1))
            return cursor.fetchone()[0]
            #cursor.execute('''SELECT usuarioVotante, usuarioVotado, composicion FROM Vota_TAB WHERE WHERE usuarioVotado = ? AND composicion = ?''', 
            #               (usuarioVotado, composicion))
            #rows = cursor.fetchall()
            #return [VotaVO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return 0
        finally:
            conn.close()

    # Encontrar votos negativos a una composición
    def find_bad_votes_to_comp(self, usuarioVotado, composicion):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(*) FROM Vota_TAB WHERE usuarioVotado = ? AND composicion = ? AND voto = ?''', 
                           (usuarioVotado, composicion, -1))
            return cursor.fetchone()[0]
            #cursor.execute('''SELECT usuarioVotante, usuarioVotado, composicion FROM Vota_TAB WHERE WHERE usuarioVotado = ? AND composicion = ?''', 
            #               (usuarioVotado, composicion))
            #rows = cursor.fetchall()
            #return [VotaVO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return 0
        finally:
            conn.close()