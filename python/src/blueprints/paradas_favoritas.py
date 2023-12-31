from flask import Blueprint, render_template, redirect, url_for

from src.database.conexion import Conexion

bp_paradas_favoritas=Blueprint("paradas_favoritas", __name__)

@bp_paradas_favoritas.route("/paradas_favoritas", methods=["GET"])
def obtenerParadasFavoritas():

	conexion=Conexion()

	paradas_favoritas=conexion.obtenerParadasFavoritas()

	conexion.cerrarConexion()

	return render_template("paradas_favoritas.html", paradas_favoritas=paradas_favoritas)

@bp_paradas_favoritas.route("/eliminar_parada_favorita/<id_parada>", methods=["GET"])
def eliminarParadaFavorita(id_parada):

	conexion=Conexion()

	conexion.eliminarParadaFavorita(id_parada)

	conexion.cerrarConexion()

	return redirect(url_for("paradas_favoritas.obtenerParadasFavoritas"))

@bp_paradas_favoritas.route("/ver_parada_favorita/<id_parada>", methods=["GET"])
def verParadaFavorita(id_parada):

	conexion=Conexion()

	latitud, longitud=conexion.obtenerCoordenadasParada(id_parada)

	nombre, parada=conexion.obtenerInformacionParada(id_parada)

	conexion.cerrarConexion()

	return render_template("mapa_parada.html", latitud=latitud, longitud=longitud, nombre=nombre, parada=parada)