import sqlite3

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
            conn = sqlite3.connect('db/database.db')
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