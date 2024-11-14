CREATE TRIGGER after_delete_composicion
AFTER DELETE ON Composicion_TAB
FOR EACH ROW
BEGIN
    -- Eliminar las filas relacionadas en Vota_TAB
    DELETE FROM Vota_TAB 
    WHERE usuarioVotado = OLD.usuario 
      AND composicion = OLD.nombre;

    -- Eliminar las filas relacionadas en Formada_por_TAB
    DELETE FROM Formada_por_TAB 
    WHERE usuario = OLD.usuario 
      AND composicion = OLD.nombre;
END;

CREATE TRIGGER after_delete_usuario
AFTER DELETE ON Usuario_TAB
FOR EACH ROW
BEGIN
    -- Eliminar las filas relacionadas en Reporta_TAB
    DELETE FROM Reporta_TAB 
    WHERE usuarioReportador = OLD.mail 
       OR usuarioReportado = OLD.mail;

    -- Eliminar las filas relacionadas en Vota_TAB
    DELETE FROM Vota_TAB 
    WHERE usuarioVotante = OLD.mail 
       OR usuarioVotado = OLD.mail;

    -- Eliminar las filas relacionadas en Composicion_TAB
    DELETE FROM Composicion_TAB 
    WHERE usuario = OLD.mail;
END;