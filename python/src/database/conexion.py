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