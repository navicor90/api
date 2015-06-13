import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_restful import Api
from flask.ext.restful.representations.json import output_json
from flask.ext.cors import CORS

from app.mod_shared.models import db
from app.mod_profiles.models import *
from app.mod_profiles.resources import *
from . import config

output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

db.app = app
db.init_app(app)

# Manejo global de solicitudes CORS
cors = CORS(app)

api = Api(app)

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

from app import views
