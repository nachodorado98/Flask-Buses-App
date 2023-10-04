from flask import Blueprint, render_template, request, redirect, url_for

from src.database.conexion import Conexion

bp_anadir_paradas=Blueprint("anadir_paradas", __name__)

@bp_anadir_paradas.route("/seleccionar_parada/<linea>", methods=["GET"])
def anadirParada(linea):

	conexion=Conexion()

	paradas_no_favoritas=conexion.obtenerParadasNoFavoritas(linea)

	conexion.cerrarConexion()

	return render_template("anadir_parada.html", linea=linea, paradas_no_favoritas=paradas_no_favoritas)

@bp_anadir_paradas.route("/insertar_parada", methods=["POST"])
def insertarParada():

	id_parada=request.form.get("id_parada")

	conexion=Conexion()

	conexion.anadirParadaFavorita(id_parada)

	conexion.cerrarConexion()

	return redirect(url_for("inicio.inicio"))