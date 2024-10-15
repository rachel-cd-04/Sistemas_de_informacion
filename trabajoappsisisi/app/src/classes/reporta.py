import sqlite3

# VO
####
class ReportaVO:
    def __init__(self, usuarioReportador, usuarioReportado):
        self.usuarioReportador = usuarioReportador
        self.usuarioReportado = usuarioReportado

# DAO
#####
class ReportaDAO:
    # Crear un nuevo reporte en la base de datos
    def save_reporta(self, reporta):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Reporta_TAB (usuarioReportador, usuarioReportado) VALUES (?, ?)''', 
                           (reporta.usuarioReportador, reporta.usuarioReportado))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Eliminar un reporte de la base de datos
    def delete_reporta(self, usuarioReportador, usuarioReportado):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Reporta_TAB WHERE usuarioReportador = ? AND usuarioReportado = ?''', 
                           (usuarioReportador, usuarioReportado))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    # Encontrar un reporte por su id
    def find_reporta_by_id(self, usuarioReportador, usuarioReportado):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT usuarioReportador, usuarioReportado FROM Reporta_TAB WHERE usuarioReportador = ? AND usuarioReportado = ?''', 
                           (usuarioReportador, usuarioReportado))
            row = cursor.fetchone()
            if row:
                return ReportaVO(row[0], row[1], row[2])
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()