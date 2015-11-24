# -*- coding: utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api
from flask_restful_swagger import swagger
from flask.ext.restful.representations.json import output_json
from flask.ext.cors import CORS
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flaskext.uploads import configure_uploads

# Configuración de Flask-Admin con Flask-Login
from flask import url_for, redirect, render_template, request
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose

from app.mod_shared.models.db import db
from app.mod_profiles import models
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

# por ahora lo coloco acá pero debería ir en la parte del config.
configure_uploads(app, config.Config.uploaded_photos)

db.app = app
db.init_app(app)

# Configuración de migraciones de la base de datos.
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Manejo global de solicitudes CORS
cors = CORS(app)

# Importación del manejo de autenticación HTTP.
from .mod_shared.models import auth

# Crea la API y activa el soporte de Swagger para la misma.
api = swagger.docs(Api(app))

api.add_resource(AnalysisAnalysisFileList, '/analysis/<int:analysis_id>/files')
api.add_resource(AnalysisAnalysisCommentList, '/analysis/<int:analysis_id>/comments')
api.add_resource(AnalysisCommentView, '/analysis_comments/<int:analysis_comment_id>')
api.add_resource(AnalysisView, '/analysis/<int:analysis_id>')
api.add_resource(AnalysisList, '/analysis')
api.add_resource(AnalysisFileDownload, '/analysis_files/<int:id>/download')
api.add_resource(AnalysisFileThumbnail, '/analysis_files/<int:analysis_file_id>/thumbnail')
api.add_resource(AnalysisFileThumbnailByQuery, '/analysis_files/<int:analysis_file_id>/thumbnail_by_query')
api.add_resource(AnalysisFileView, '/analysis_files/<int:id>')
api.add_resource(AnalysisFileList, '/analysis_files')
api.add_resource(AnalysisGroupPermissionList, '/analysis/<int:analysis_id>/group_permissions')
api.add_resource(AnalysisMeasurementList, '/analysis/<int:analysis_id>/measurements')
api.add_resource(AnalysisPermissionList, '/analysis/<int:analysis_id>/permissions')
api.add_resource(GenderView, '/genders/<int:id>')
api.add_resource(GenderList, '/genders')
api.add_resource(GroupGroupMembershipList, '/groups/<int:group_id>/members')
api.add_resource(GroupList, '/groups')
api.add_resource(GroupMembershipView, '/group_memberships/<int:group_membership_id>')
api.add_resource(GroupPermissionView, '/group_permissions/<int:group_permission_id>')
api.add_resource(GroupView, '/groups/<int:group_id>')
api.add_resource(GroupMembershipTypeList, '/group_membership_types')
api.add_resource(GroupMembershipTypeView, '/group_membership_types/<int:group_membership_type_id>')
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
api.add_resource(NotificationView, '/notifications/<int:notification_id>')
api.add_resource(PermissionTypeList, '/permission_types')
api.add_resource(PermissionTypeView, '/permission_types/<int:permission_type_id>')
api.add_resource(PermissionView, '/permissions/<int:permission_id>')
api.add_resource(ProfileGravatarView, '/profiles/<int:profile_id>/gravatar')
api.add_resource(StorageCredentialView, '/storage_credentials/<int:id>')
api.add_resource(StorageCredentialList, '/storage_credentials')
api.add_resource(StorageLocationView, '/storage_locations/<int:id>')
api.add_resource(StorageLocationList, '/storage_locations')
api.add_resource(UserGravatarView, '/users/<int:user_id>/gravatar')
api.add_resource(UsernameCheckView, '/username_check')
api.add_resource(UserView, '/users/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(TypeUnitValidationList, '/measurement_types/<int:measurement_type_id>/unit_validations')
api.add_resource(TypeUnitValidationView, '/type_unit_validations/<int:type_unit_validation_id>')
api.add_resource(Token, '/token')

api.add_resource(MyAnalysisList, '/my/analyses')
api.add_resource(MyGravatarView, '/my/gravatar')
api.add_resource(MyLatestMeasurementList, '/my/measurements/latest')
api.add_resource(MyGroupList, '/my/groups')
api.add_resource(MyGroupMembershipList, '/my/group_memberships')
api.add_resource(MyMeasurementList, '/my/measurements')
api.add_resource(MyNotificationList, '/my/notifications')
api.add_resource(MyProfileView, '/my/profile')
api.add_resource(MySharedAnalysesList, '/my/shared_analyses')
api.add_resource(MySharedAnalysisProfileList, '/my/shared_analysis_profiles')
api.add_resource(MyStatisticsView, '/my/statistics')
api.add_resource(MyStorageCredentialList, '/my/storage_credentials')
api.add_resource(MyUserView, '/my/user')
api.add_resource(ProfileLatestMeasurementList, '/profiles/<int:profile_id>/measurements/latest')
api.add_resource(ProfileMeasurementList, '/profiles/<int:profile_id>/measurements')



# Configuración de Flask-Admin con Flask-Login

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not user.verify_password(self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(models.User).filter_by(username=self.login.data).first()

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(models.User).get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized model view class
class UserView(MyModelView):
    can_create = False
    column_exclude_list = [
        'rsa_private_key',
    ]


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


# Flask views
@app.route('/')
def index():
    return render_template('index.html')


# Initialize flask-login
init_login()

# Crea el sitio de administración.
# Create admin
admin = Admin(app,
              name='YesDoc Admin',
              index_view=MyAdminIndexView(),
              base_template='my_master.html',
              template_mode='bootstrap3')

# Add view
admin.add_view(MyModelView(models.Gender, db.session))
admin.add_view(MyModelView(models.GroupMembershipType, db.session))
admin.add_view(MyModelView(models.MeasurementSource, db.session))
admin.add_view(MyModelView(models.MeasurementType, db.session))
admin.add_view(MyModelView(models.MeasurementUnit, db.session))
admin.add_view(MyModelView(models.PermissionType, db.session))
admin.add_view(MyModelView(models.StorageLocation, db.session))
admin.add_view(MyModelView(models.TypeUnitValidation, db.session))
admin.add_view(UserView(models.User, db.session))

from . import views
