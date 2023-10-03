from flask import Blueprint, render_template

from src.database.conexion import Conexion

bp_inicio=Blueprint("inicio", __name__)

@bp_inicio.route("/", methods=["GET"])
def inicio():

	conexion=Conexion()

	lineas_recorridas=conexion.obtenerLineasRecorridas()

	conexion.cerrarConexion()

	return render_template("inicio.html", lineas_recorridas=lineas_recorridas)