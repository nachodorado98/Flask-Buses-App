import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para cconfirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para obtener las lineas recorridas
	def obtenerLineasRecorridas(self, recorrida:bool=True)->Optional[List[tuple]]:

		if recorrida:

			self.c.execute("""SELECT Linea, Inicio, Fin
								FROM lineas
								WHERE Recorrida=True
								ORDER BY Id_Linea""")
		else:

			self.c.execute("""SELECT Linea, Inicio, Fin
								FROM lineas
								WHERE Recorrida=False
								ORDER BY Id_Linea""")

		lineas=self.c.fetchall()

		return list(map(lambda linea: (linea["linea"], linea["inicio"], linea["fin"]), lineas)) if lineas else None

	# Metodo para añadir una linea a recorrida
	def anadirLineaRecorrida(self, linea:str)->None:

		self.c.execute("""UPDATE lineas
							SET Recorrida=True
							WHERE Linea=%s""",
							(linea,))

		self.confirmar()

	# Metodo para obtener el detalle de una linea
	def obtenerDetalleLinea(self, linea:str)->Optional[tuple]:

		self.c.execute("""SELECT Inicio, Fin, Tipo
							FROM lineas
							WHERE Linea=%s""",
							(linea,))

		linea=self.c.fetchone()

		return None if linea is None else (linea["inicio"], linea["fin"], linea["tipo"])

	# Metodo para obtener numero de paradas de una linea
	def obtenerNumeroParadas(self, linea:str)->Optional[int]:

		self.c.execute("""SELECT COUNT(p.Parada) as Numero_paradas
							FROM lineas l
							JOIN paradas p
							USING(Id_Linea)
							GROUP BY Id_Linea
							HAVING Linea=%s""",
							(linea,))

		paradas=self.c.fetchone()

		return None if paradas is None else paradas["numero_paradas"]

	# Metodo para obtener las paradas de una linea que no son favoritas
	def obtenerParadasNoFavoritas(self, linea:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT p.Id_Parada, p.Parada, p.Nombre, p.Sentido
							FROM lineas l
							JOIN paradas p
							USING(Id_Linea)
							WHERE l.Linea=%s
							AND Favorita=False
							ORDER BY p.Sentido, p.Parada;""",
							(linea,))

		paradas=self.c.fetchall()

		return list(map(lambda parada: (parada["id_parada"], parada["parada"], parada["nombre"], parada["sentido"]), paradas)) if paradas else None

	# Metodo para añadir una parada a favorita
	def anadirParadaFavorita(self, id_parada:int)->None:

		self.c.execute("""UPDATE paradas
							SET Favorita=True
							WHERE Id_Parada=%s""",
							(id_parada,))

		self.confirmar()