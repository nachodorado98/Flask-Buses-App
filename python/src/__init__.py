from flask import Flask

from .blueprints.inicio import bp_inicio
from .blueprints.anadir_lineas import bp_anadir_lineas
from .blueprints.detalle_linea import bp_detalle_linea
from .blueprints.anadir_paradas import bp_anadir_paradas
from .blueprints.paradas_favoritas import bp_paradas_favoritas
from .blueprints.ver_recorrido import bp_ver_recorrido

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_anadir_lineas)
	app.register_blueprint(bp_detalle_linea)
	app.register_blueprint(bp_anadir_paradas)
	app.register_blueprint(bp_paradas_favoritas)
	app.register_blueprint(bp_ver_recorrido)

	return app