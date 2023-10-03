import pytest

@pytest.mark.parametrize(["linea"],
	[("N2",),("N17",),("M1",),("T61",),("C2",),("H",)]
)
def test_pagina_detalle_linea_no_paradas(cliente, conexion, linea):

	respuesta=cliente.get(f"/detalle_linea/{linea}")

	contenido=respuesta.data.decode()

	print(contenido)

	respuesta.status_code==200
	assert "Detalle de la linea" in contenido
	assert linea in contenido
	assert "Autobus" in contenido
	assert "No hay informacion de las paradas de esta linea." in contenido
	assert "Numero de paradas:" not in contenido

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("35",),("310",)]
)
def test_pagina_detalle_linea(cliente, conexion, linea):

	respuesta=cliente.get(f"/detalle_linea/{linea}")

	contenido=respuesta.data.decode()

	print(contenido)

	respuesta.status_code==200
	assert "Detalle de la linea" in contenido
	assert linea in contenido
	assert "Autobus" in contenido
	assert "No hay informacion de las paradas de esta linea." not in contenido
	assert "Numero de paradas:" in contenido