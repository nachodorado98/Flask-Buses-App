from flask import Blueprint, render_template

from src.database.conexion import Conexion

bp_ver_recorrido=Blueprint("ver_recorrido", __name__)

@bp_ver_recorrido.route("/ver_recorrido/<linea>", methods=["GET"])
def verRecorrido(linea):

	conexion=Conexion()

	paradas_ida=conexion.obtenerRecorrido(linea)

	paradas_vuelta=conexion.obtenerRecorrido(linea, ida=False)

	conexion.cerrarConexion()

	return render_template("mapa_recorrido.html", linea=linea, paradas_ida=paradas_ida, paradas_vuelta=paradas_vuelta)