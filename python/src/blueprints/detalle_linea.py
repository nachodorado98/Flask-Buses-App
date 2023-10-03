from flask import Blueprint, render_template

from src.database.conexion import Conexion

bp_detalle_linea=Blueprint("detalle_linea", __name__)

@bp_detalle_linea.route("/detalle_linea/<linea>", methods=["GET"])
def obtenerDetalleLinea(linea):

	conexion=Conexion()

	inicio, fin, tipo=conexion.obtenerDetalleLinea(linea)

	numero_paradas=conexion.obtenerNumeroParadas(linea)

	conexion.cerrarConexion()

	return render_template("detalle.html", linea=linea, inicio=inicio, fin=fin, tipo=tipo, numero_paradas=numero_paradas)