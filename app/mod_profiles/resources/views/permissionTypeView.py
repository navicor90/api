# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import PermissionType
from app.mod_profiles.common.fields.permissionTypeFields import PermissionTypeFields
from app.mod_profiles.common.parsers.permissionType import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class PermissionTypeView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de tipo de permiso.'.encode('utf-8'),
        responseClass='PermissionTypeFields',
        nickname='permissionTypeView_get',
        parameters=[
            {
                "name": "id",
                "description": u'Identificador único del tipo de permiso.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            }
        ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @marshal_with(PermissionTypeFields.resource_fields, envelope='resource')
    def get(self, permission_type_id):
        permission_type = PermissionType.query.get_or_404(permission_type_id)
        return permission_type

    @swagger.operation(
        notes=u'Actualiza una instancia específica de tipo de permiso, y la retorna.'.encode('utf-8'),
        responseClass='PermissionTypeFields',
        nickname='permissionTypeView_put',
        parameters=[
            {
                "name": "id",
                "description": u'Identificador único del tipo de permiso.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "name",
                "description": u'Nombre del tipo de permiso.'.encode('utf-8'),
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "description",
                "description": u'Descripción del tipo de permiso.'.encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "can_view_analysis_files",
                "description": (u'Permiso para visualizar los archivos del '
                                'análisis.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },
            {
                "name": "can_view_measurements",
                "description": (u'Permiso para visualizar las mediciones del '
                                'análisis.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },
            {
                "name": "can_edit_analysis_files",
                "description": (u'Permiso para editar los archivos del '
                                'análisis.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },
            {
                "name": "can_edit_measurements",
                "description": (u'Permiso para editar las mediciones del '
                                'análisis.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(PermissionTypeFields.resource_fields, envelope='resource')
    def put(self, permission_type_id):
        # Obtiene el tipo de permiso.
        permission_type = PermissionType.query.get_or_404(permission_type_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        name = args['name']
        description = args['description']
        can_view_analysis_files = args['can_view_analysis_files']
        can_view_measurements = args['can_view_measurements']
        can_edit_analysis_files = args['can_edit_analysis_files']
        can_edit_measurements = args['can_edit_measurements']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (name is not None and
                permission_type.name != name):
            permission_type.name = name
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (description is not None and
                permission_type.description != description):
            permission_type.description = description
        # Actualiza el permiso de visualización de archivos del análisis, en
        # caso de que haya sido modificado.
        if (can_view_analysis_files is not None and
                permission_type.can_view_analysis_files != can_view_analysis_files):
            permission_type.can_view_analysis_files = can_view_analysis_files
        # Actualiza el permiso de visualización de mediciones del análisis, en
        # caso de que haya sido modificado.
        if (can_view_measurements is not None and
                permission_type.can_view_measurements != can_view_measurements):
            permission_type.can_view_measurements = can_view_measurements
        # Actualiza el permiso de edición de archivos del análisis, en
        # caso de que haya sido modificado.
        if (can_edit_analysis_files is not None and
                permission_type.can_edit_analysis_files != can_edit_analysis_files):
            permission_type.can_edit_analysis_files = can_edit_analysis_files
        # Actualiza el permiso de edición de mediciones del análisis, en
        # caso de que haya sido modificado.
        if (can_edit_measurements is not None and
                permission_type.can_edit_measurements != can_edit_measurements):
            permission_type.can_edit_measurements = can_edit_measurements

        db.session.commit()
        return permission_type, 200
