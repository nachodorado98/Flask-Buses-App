import pytest

def test_pagina_anadir_lineas(cliente, conexion):

	respuesta=cliente.get("/anadir_linea")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Añadir linea recorrida" in contenido
	assert "Selecciona una de las lineas" in contenido

def test_pagina_anadir_lineas_todas_recorridas(cliente, conexion):

	conexion.c.execute("""UPDATE lineas
						SET Recorrida=True""")

	conexion.confirmar()

	respuesta=cliente.get("/anadir_linea")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Añadir linea recorrida" in contenido
	assert "Selecciona una de las lineas" not in contenido
	assert "!ENHORABUENA¡" in contenido
	assert "Ya no hay ninguna linea por recorrer." in contenido
	assert "Has recorrido todas las lineas existentes." in contenido

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("N17",),("M1",)]
)
def test_pagina_insertar_lineas(cliente, linea):

	respuesta=cliente.post("/insertar_linea", data={"linea":linea})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido