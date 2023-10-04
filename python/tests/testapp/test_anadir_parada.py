import pytest

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("9",),("35",)]
)
def test_pagina_anadir_paradas(cliente, conexion, linea):

	respuesta=cliente.get(f"/seleccionar_parada/{linea}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert f"Añadir parada linea {linea}" in contenido
	assert "Selecciona una de las paradas" in contenido
	assert "Cancelar" in contenido

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("9",),("35",), ("U",),("N17",)]
)
def test_pagina_anadir_lineas_todas_favoritas(cliente, conexion, linea):

	conexion.c.execute("""UPDATE paradas
						SET Favorita=True""")

	conexion.confirmar()

	respuesta=cliente.get(f"/seleccionar_parada/{linea}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert f"Añadir parada linea {linea}" in contenido
	assert "Selecciona una de las paradas" not in contenido
	assert "Cancelar" not in contenido
	assert "!VAYA" in contenido
	assert "Parece que ya no hay mas paradas de esta linea para escoger." in contenido

@pytest.mark.parametrize(["id_parada"],
	[(1,),(22,),(70,),(69,)]
)
def test_pagina_insertar_paradas(cliente, id_parada):

	respuesta=cliente.post("/insertar_parada", data={"id_parada":id_parada})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido