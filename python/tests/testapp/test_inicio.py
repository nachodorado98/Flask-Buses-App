import pytest

def test_pagina_inicial_sin_lineas_recorridas(cliente, conexion):

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Lineas de autobuses recorridas" in contenido
	assert "No hay líneas recorridas disponibles." in contenido

def test_pagina_inicial_con_lineas_recorridas(cliente, conexion):

	conexion.c.execute("""UPDATE lineas
						SET Recorrida=True
						WHERE Id_Linea=1""")

	conexion.confirmar()

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Lineas de autobuses recorridas" in contenido
	assert "No hay líneas recorridas disponibles." not in contenido
	assert "<table>" in contenido
	assert "<th>Linea</th>" in contenido
	assert "<th>Inicio de la Línea</th>" in contenido
	assert "<th>Fin de la Línea</th>" in contenido

	conexion.c.execute("""UPDATE lineas
						SET Recorrida=False
						WHERE Id_Linea=1""")

	conexion.confirmar()