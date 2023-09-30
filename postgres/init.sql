CREATE DATABASE bbdd_buses;

\c bbdd_buses;


CREATE TABLE lineas (Id_Linea INT PRIMARY KEY,
			Linea VARCHAR(20),
			Inicio VARCHAR(60),
			Fin VARCHAR(60),
			Tipo VARCHAR(15),
			Recorrida BOOL);

ALTER TABLE lineas ALTER COLUMN Recorrida SET DEFAULT FALSE;

\copy lineas (Id_Linea, Linea, Inicio, Fin, Tipo) FROM '/docker-entrypoint-initdb.d/lineas.csv' WITH CSV HEADER;

CREATE TABLE paradas(Id_Parada INT PRIMARY KEY,
			Parada INT,
			Nombre VARCHAR(100),
			Id_Linea INT,
			Sentido VARCHAR(20),
			Latitud FLOAT,
			Longitud FLOAT,
			Favorita BOOL,
			FOREIGN KEY (Id_Linea) REFERENCES lineas (Id_Linea) ON DELETE CASCADE);

ALTER TABLE paradas ALTER COLUMN Favorita SET DEFAULT FALSE;


\copy paradas (Id_Parada, Parada, Nombre, Id_Linea, Sentido, Latitud, Longitud) FROM '/docker-entrypoint-initdb.d/paradas.csv' WITH CSV HEADER;