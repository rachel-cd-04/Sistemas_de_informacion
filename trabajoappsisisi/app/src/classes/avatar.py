import sqlite3

# VO
####
class AvatarVO:
    def __init__(self, id, URL_):
        self.id = id
        self.URL_ = URL_


# DAO
#####
class AvatarDAO:
    # Encontrar avatar por su id
    def find_avatar_by_id(self, id):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT id, URL_ FROM Avatar_TAB WHERE id = ?''', 
                            (id,))
            row = cursor.fetchone()
            if row:
                return AvatarVO(row[0], row[1])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()