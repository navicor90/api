# -*- coding: latin-1 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from flask.ext.restful.representations.json import output_json
from flask.ext.cors import CORS
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app.mod_shared.models import db
from app.mod_profiles.models import User
from app.mod_profiles.resources.lists import *
from app.mod_profiles.resources.views import *
from . import config

def get_config_class(config_mode):
    """
    Determina el tipo de configuración a utilizar, a partir del modo especificado.

    En base a una cadena que especifica el modo de configuración, devuelve la
    clase apropiada que maneja ese modo de configuración.
    Por defecto, se hace uso del modo de configuración 'production'.

    Los valores posibles son (sin diferenciar minúsculas de mayúsculas):
        * Production
        * Staging
        * Development
        * Testing

    Parámetros:
    config_mode -- Modo de configuración (string)
    """
    # Lista de asociación entre modos de configuración y las clases que los
    # manejan.
    configurations = {
                      'production':  config.ProductionConfig,
                      'staging':     config.StagingConfig,
                      'development': config.DevelopmentConfig,
                      'testing':     config.TestingConfig,
                     }
    # Modo de configuración por defecto.
    default_config_mode = 'production'

    # Convierte el parámetro 'config_mode' a minúsculas, para su posterior
    # comparación.
    config_mode = config_mode.lower()
    # Establece la clase que maneja el modo especificado, o el modo por defecto
    # en caso de haberse especificado un modo inválido.
    if (config_mode in configurations):
        config_class = configurations[config_mode]
    else:
        config_class = configurations[default_config_mode]
    # Devuelve la clase establecida.
    return config_class


output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}

app = Flask(__name__)

# Obtiene la variable de entorno FLASK_CONFIG_MODE. En caso de no encontrarse
# seteada, el valor por defecto es 'production', por ser el más seguro.
flask_config_mode = os.getenv('FLASK_CONFIG_MODE', 'production')
# Configura la aplicación en base a la clase de configuración que maneja el
# modo especificado.
app.config.from_object(get_config_class(flask_config_mode))

db.app = app
db.init_app(app)

# Configuraci�n de migraciones de la base de datos.
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Manejo global de solicitudes CORS
cors = CORS(app)

# Manejo de autenticaci�n HTTP.
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # Prueba la autenticaci�n mediante token.
    user = User.verify_auth_token(username_or_token)
    if not user:
        # Prueba la autenticaci�n mediante usuario y contrase�a.
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    return True

# Crea la API y activa el soporte de Swagger para la misma.
api = swagger.docs(Api(app))

api.add_resource(GenderView, '/genders/<int:id>')
api.add_resource(GenderList, '/genders')
api.add_resource(ProfileView, '/profiles/<int:id>')
api.add_resource(ProfileList, '/profiles')
api.add_resource(MeasurementView, '/measurements/<int:id>')
api.add_resource(MeasurementList, '/measurements')
api.add_resource(MeasurementSourceView, '/measurement_sources/<int:id>')
api.add_resource(MeasurementSourceList, '/measurement_sources')
api.add_resource(MeasurementTypeView, '/measurement_types/<int:id>')
api.add_resource(MeasurementTypeList, '/measurement_types')
api.add_resource(MeasurementUnitView, '/measurement_units/<int:id>')
api.add_resource(MeasurementUnitList, '/measurement_units')

api.add_resource(MeasurementTypeUnitsList, '/measurement_types/<int:id>/units')
api.add_resource(ProfileLatestMeasurementList, '/profiles/<int:profile_id>/measurements/latest')
api.add_resource(ProfileMeasurementList, '/profiles/<int:profile_id>/measurements')

from . import views
