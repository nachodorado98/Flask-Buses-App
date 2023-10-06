import pytest

def test_pagina_paradas_favoritas_sin_paradas_favoritas(cliente, conexion):

	respuesta=cliente.get("/paradas_favoritas")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Paradas favoritas" in contenido
	assert "No hay paradas favoritas aún." in contenido

def test_pagina_paradas_favoritas_con_paradas_favoritas(cliente, conexion):

	cliente.post("/insertar_parada", data={"id_parada":210})

	respuesta=cliente.get("/paradas_favoritas")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Paradas favoritas" in contenido
	assert "No hay paradas favoritas aún." not in contenido
	assert "<table>" in contenido
	assert "<th>Linea</th>" in contenido
	assert "<th>Parada</th>" in contenido
	assert "<th>Nombre de la parada</th>" in contenido
	assert "<th>Sentido</th>" in contenido

@pytest.mark.parametrize(["id_parada"],
	[(1,),(22,),(70,),(13,)]
)
def test_pagina_eliminar_paradas(cliente, conexion, id_parada):

	cliente.post("/insertar_parada", data={"id_parada":id_parada})

	respuesta=cliente.get(f"/eliminar_parada_favorita/{id_parada}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/paradas_favoritas"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["id_parada"],
	[(1,),(22,),(70,),(13,)]
)
def test_pagina_ver_parada(cliente, conexion, id_parada):

	respuesta=cliente.get(f"/ver_parada_favorita/{id_parada}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Mapa parada" in contenido