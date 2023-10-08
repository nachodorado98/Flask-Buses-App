import pytest

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("35",),("9",),("139",)]
)
def test_pagina_ver_parada(cliente, conexion, linea):

	respuesta=cliente.get(f"/ver_recorrido/{linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"Mapa recorrido linea {linea}" in contenido
	assert "Leyenda Recorrido" in contenido