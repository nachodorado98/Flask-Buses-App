from flask import Blueprint, render_template, request, redirect, url_for

from src.database.conexion import Conexion

bp_anadir_lineas=Blueprint("anadir_lineas", __name__)

@bp_anadir_lineas.route("/anadir_linea", methods=["GET"])
def anadirLinea():

	conexion=Conexion()

	lineas_no_recorridas=conexion.obtenerLineasRecorridas(recorrida=False)

	conexion.cerrarConexion()

	return render_template("anadir.html", lineas_no_recorridas=lineas_no_recorridas)

@bp_anadir_lineas.route("/insertar_linea", methods=["POST"])
def insertarLinea():

	linea=request.form.get("linea")

	conexion=Conexion()

	conexion.anadirLineaRecorrida(linea)

	conexion.cerrarConexion()

	return redirect(url_for("inicio.inicio"))