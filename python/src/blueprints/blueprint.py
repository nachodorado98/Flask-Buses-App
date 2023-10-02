from flask import Blueprint, render_template

from src.database.conexion import Conexion

bp=Blueprint("blueprint", __name__)

# Vista de la pagina principal
@bp.route("/", methods=["GET"])
def inicio()->str:

	conexion=Conexion()

	lineas_recorridas=conexion.obtenerLineasRecorridas()

	return render_template("inicio.html", lineas_recorridas=lineas_recorridas)