import sqlite3

DB_PATH = '/app/src/db/database.db'

# VO
####
class PoseeVO:
    def __init__(self, campeon, sinergia):
        self.campeon = campeon
        self.sinergia = sinergia


# DAO
#####
class PoseeDAO:
    # Encontrar la relacion entre campeon y sinergia por su id
    def find_posee_by_id(self, campeon, sinergia):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT campeon, sinergia FROM Posee_TAB WHERE campeon = ? AND sinergia = ?''', 
                           (campeon, sinergia))
            row = cursor.fetchone()
            if row:
                return PoseeVO(row[0], row[1])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    def get_sinergias_by_champion_id(self, campeon):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT sinergia FROM Posee_TAB WHERE campeon = ?''', (campeon,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()