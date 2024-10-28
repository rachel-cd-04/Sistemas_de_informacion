CREATE TABLE Usuario_TAB (
    mail VARCHAR(200) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    contra VARCHAR(200) NOT NULL,
    avatar INTEGER,
    FOREIGN KEY(avatar) REFERENCES Avatar_TAB(id) ON DELETE CASCADE
);

CREATE TABLE Avatar_TAB (
    id INTEGER PRIMARY KEY, -- Clave primaria 
    URL_ VARCHAR(200) NOT NULL
);

CREATE TABLE Composicion_TAB (
    usuario VARCHAR(200),
    nombre VARCHAR(200) NOT NULL,
    dificultad VARCHAR(200) NOT NULL,
    publicado VARCHAR(1) NOT NULL,
    descr VARCHAR(200) NOT NULL,
    FOREIGN KEY(usuario) REFERENCES Usuario_TAB(mail) ON DELETE CASCADE,
    CONSTRAINT composicion_PK PRIMARY KEY (usuario, nombre)
);

CREATE TABLE Campeon_TAB (
	nombre VARCHAR(200) NOT NULL PRIMARY KEY,
    url_buscador VARCHAR(200) NOT NULL,
    url_campo VARCHAR(200) NOT NULL,
    url_recom VARCHAR(200) NOT NULL,
    coste INTEGER
);

CREATE TABLE Sinergia_TAB (
	nombre VARCHAR(200) NOT NULL PRIMARY KEY,
    url_ VARCHAR(200) NOT NULL,
    unidades_mejora VARCHAR(200) NOT NULL
);

CREATE TABLE Vota_TAB (
    usuarioVotante VARCHAR(200),
    usuarioVotado VARCHAR(200),
    composicion VARCHAR(200),
    FOREIGN KEY(usuarioVotante) REFERENCES Usuario_TAB(mail) ON DELETE CASCADE,
    FOREIGN KEY(usuarioVotado, composicion) REFERENCES Composicion_TAB(usuario, nombre) ON DELETE CASCADE,
    CONSTRAINT vota_PK PRIMARY KEY (usuarioVotante, usuarioVotado, composicion)
);

CREATE TABLE Formada_por_TAB (
    usuario VARCHAR(200),
    composicion VARCHAR(200),
    campeon VARCHAR(200),
    FOREIGN KEY(usuario, composicion) REFERENCES Composicion_TAB(usuario, nombre) ON DELETE CASCADE,
    FOREIGN KEY(campeon) REFERENCES Campeon_TAB(nombre) ON DELETE CASCADE,
    CONSTRAINT formada_por_PK PRIMARY KEY (usuario, composicion, campeon)
);

CREATE TABLE Posee_TAB (
    campeon VARCHAR(200),
    sinergia VARCHAR(200),
    FOREIGN KEY(campeon) REFERENCES Campeon_TAB(nombre) ON DELETE CASCADE,
    FOREIGN KEY(sinergia) REFERENCES Sinergia_TAB(nombre) ON DELETE CASCADE,
    CONSTRAINT posee_PK PRIMARY KEY (campeon, sinergia)
);

CREATE TABLE Emblema_TAB (
    nombre VARCHAR(200) NOT NULL PRIMARY KEY,
    url_ VARCHAR(200) NOT NULL,
    sinergia VARCHAR(200),
    FOREIGN KEY(sinergia) REFERENCES Sinergia_TAB(nombre) ON DELETE CASCADE
);

CREATE TABLE Reporta_TAB (
    usuarioReportador VARCHAR(200),
    usuarioReportado VARCHAR(200),
    FOREIGN KEY(usuarioReportador) REFERENCES Usuario_TAB(mail) ON DELETE CASCADE,
    FOREIGN KEY(usuarioReportado) REFERENCES Usuario_TAB(mail) ON DELETE CASCADE,
    CONSTRAINT reporta_PK PRIMARY KEY (usuarioReportador, usuarioReportado)
);
