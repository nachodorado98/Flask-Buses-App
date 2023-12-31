import pytest

def test_tabla_lineas_llena(conexion):

	conexion.c.execute("SELECT * FROM lineas")

	assert conexion.c.fetchall()!=[]

def test_tabla_paradas_llena(conexion):

	conexion.c.execute("SELECT * FROM paradas")

	assert conexion.c.fetchall()!=[]

def test_obtener_lineas_recorridas_no_existentes(conexion):

	assert conexion.obtenerLineasRecorridas() is None

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_obtener_lineas_recorridas_existente(conexion, id_linea):

	conexion.c.execute(f"""UPDATE lineas
						SET Recorrida=True
						WHERE Id_Linea={id_linea}""")

	conexion.confirmar()

	lineas=conexion.obtenerLineasRecorridas()

	assert len(lineas)==1
	assert lineas[0][0]==str(id_linea)

def test_obtener_lineas_recorridas(conexion):

	for numero in range(1,6):

		conexion.c.execute(f"""UPDATE lineas
							SET Recorrida=True
							WHERE Id_Linea={numero}""")

	conexion.confirmar()

	lineas=conexion.obtenerLineasRecorridas()

	assert len(lineas)==5

	for numero, linea in enumerate(lineas):

		assert linea[0]==str(numero+1)

def test_obtener_lineas_no_recorridas_no_existentes(conexion):

	conexion.c.execute("""UPDATE lineas
						SET Recorrida=True""")

	conexion.confirmar()

	assert conexion.obtenerLineasRecorridas(recorrida=False) is None

def test_obtener_lineas_no_recorridas(conexion):

	lineas=conexion.obtenerLineasRecorridas(recorrida=False)

	assert len(lineas)==209

def test_obtener_lineas_no_recorridas_varias_recorridas(conexion):

	for numero in range(1,6):

		conexion.c.execute(f"""UPDATE lineas
							SET Recorrida=True
							WHERE Id_Linea={numero}""")

	conexion.confirmar()

	lineas=conexion.obtenerLineasRecorridas(recorrida=False)

	assert len(lineas)==204

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("N17",),("M1",)]
)
def test_anadir_linea_recorrida(conexion, linea):

	conexion.anadirLineaRecorrida(linea)

	lineas=conexion.obtenerLineasRecorridas()

	assert len(lineas)==1

	conexion.c.execute("""SELECT Recorrida
							FROM lineas
							WHERE Linea=%s""",
							(linea,))

	assert conexion.c.fetchone()["recorrida"]

@pytest.mark.parametrize(["linea"],
	[("13",),("90",),("91",),("99",),("1000",),("S",)]
)
def test_obtener_detalle_linea_no_existe(conexion, linea):

	assert conexion.obtenerDetalleLinea(linea) is None

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("N17",),("M1",)]
)
def test_obtener_detalle_linea(conexion, linea):

	assert conexion.obtenerDetalleLinea(linea) is not None

@pytest.mark.parametrize(["linea"],
	[("13",),("90",),("N2",),("M1",),("SE661",)]
)
def test_obtener_paradas_linea_no_tiene(conexion, linea):

	assert conexion.obtenerNumeroParadas(linea) is None

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("47",),("35",)]
)
def test_obtener_paradas_linea(conexion, linea):

	assert conexion.obtenerNumeroParadas(linea) is not None

@pytest.mark.parametrize(["linea"],
	[("13",),("S",),("90",),("99",),("1000",)]
)
def test_obtener_paradas_linea_no_existente(conexion, linea):

	assert conexion.obtenerParadasNoFavoritas(linea) is None

@pytest.mark.parametrize(["linea", "cantidad"],
	[
		("1", 57),
		("34", 82),
		("139", 47),
		("9", 71)
	]
)
def test_obtener_paradas_linea_sin_favoritas(conexion, linea, cantidad):

	paradas=conexion.obtenerParadasNoFavoritas(linea)

	assert len(paradas)==cantidad

@pytest.mark.parametrize(["linea", "id_parada", "cantidad"],
	[
		("1", 210, 57),
		("34", 232, 82),
		("139", 852, 47),
		("9", 212, 71)
	]
)
def test_obtener_paradas_linea_con_favorita(conexion, linea, id_parada, cantidad):

	conexion.c.execute(f"""UPDATE paradas
							SET Favorita=True
							WHERE Id_Parada={id_parada}""")

	conexion.confirmar()

	paradas=conexion.obtenerParadasNoFavoritas(linea)

	assert len(paradas)==cantidad-1

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("9",),("139",),("47",),("35",)]
)
def test_obtener_paradas_linea_todas_favoritas(conexion, linea):

	conexion.c.execute("""UPDATE paradas
							SET Favorita=True""")

	conexion.confirmar()

	assert conexion.obtenerParadasNoFavoritas(linea) is None

def test_anadir_parada_favorita(conexion):

	assert len(conexion.obtenerParadasNoFavoritas("1"))==57

	conexion.anadirParadaFavorita(210)

	paradas=conexion.obtenerParadasNoFavoritas("1")

	assert len(paradas)==56

	conexion.c.execute("""SELECT Favorita
							FROM paradas
							WHERE Id_Parada=210""")

	assert conexion.c.fetchone()["favorita"]

def test_obtener_paradas_favoritas_no_existentes(conexion):

	assert conexion.obtenerParadasFavoritas() is None

def test_obtener_paradas_favoritas_existente(conexion):

	conexion.anadirParadaFavorita(210)

	favoritas=conexion.obtenerParadasFavoritas()

	assert len(favoritas)==1

def test_obtener_paradas_favoritas_existentes(conexion):

	for id_parada in range(1,101):

		conexion.anadirParadaFavorita(id_parada)

	favoritas=conexion.obtenerParadasFavoritas()

	assert len(favoritas)==100

def test_eliminar_parada_favorita(conexion):

	conexion.anadirParadaFavorita(210)

	conexion.c.execute("""SELECT Favorita
							FROM paradas
							WHERE Id_Parada=210""")

	assert conexion.c.fetchone()["favorita"]

	conexion.eliminarParadaFavorita(210)

	conexion.c.execute("""SELECT Favorita
							FROM paradas
							WHERE Id_Parada=210""")

	assert not conexion.c.fetchone()["favorita"]

@pytest.mark.parametrize(["id_parada"],
	[(0,),(-1,),(8356,),(10000,)]
)
def test_obtener_coordenadas_parada_no_existente(conexion, id_parada):

	assert conexion.obtenerCoordenadasParada(id_parada) is None

@pytest.mark.parametrize(["id_parada"],
	[(10,),(1,),(8355,),(1000,)]
)
def test_obtener_coordenadas_parada(conexion, id_parada):

	coordenadas=conexion.obtenerCoordenadasParada(id_parada)

	assert len(coordenadas)==2

@pytest.mark.parametrize(["id_parada"],
	[(0,),(-1,),(8356,),(10000,)]
)
def test_obtener_informacion_parada_no_existente(conexion, id_parada):

	assert conexion.obtenerInformacionParada(id_parada) is None

@pytest.mark.parametrize(["id_parada"],
	[(10,),(1,),(8355,),(1000,)]
)
def test_obtener_informacion_parada(conexion, id_parada):

	informacion=conexion.obtenerInformacionParada(id_parada)

	assert len(informacion)==2

@pytest.mark.parametrize(["linea"],
	[("13",),("S",),("N17",),("M1",),("1000",)]
)
def test_obtener_paradas_linea_sentido_no_existen(conexion, linea):

	assert conexion.obtenerRecorrido(linea) is None

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("35",),("9",),("139",)]
)
def test_obtener_paradas_linea_sentido_ida(conexion, linea):

	paradas=conexion.obtenerRecorrido(linea)

	for parada in paradas:

		assert "Ida" in parada
		assert "Vuelta" not in parada

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("35",),("9",),("139",)]
)
def test_obtener_paradas_linea_sentido_vuelta(conexion, linea):

	paradas=conexion.obtenerRecorrido(linea, ida=False)

	for parada in paradas:

		assert "Ida" not in parada
		assert "Vuelta" in parada

@pytest.mark.parametrize(["linea"],
	[("1",),("34",),("35",),("9",),("139",)]
)
def test_obtener_paradas_linea_ambos_sentido(conexion, linea):

	paradas_ida=conexion.obtenerRecorrido(linea)

	paradas_vuelta=conexion.obtenerRecorrido(linea, ida=False)

	paradas_total=conexion.obtenerNumeroParadas(linea)

	assert paradas_total==len(paradas_ida)+len(paradas_vuelta)