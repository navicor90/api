# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import PermissionType
from app.mod_profiles.common.fields.permissionTypeFields import PermissionTypeFields
from app.mod_profiles.common.parsers.permissionType import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created


class PermissionTypeList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de tipo de permiso.'.encode('utf-8'),
        responseClass='PermissionTypeFields',
        nickname='permissionTypeList_get',
        responseMessages=[
            code_200_ok
        ]
    )
    @marshal_with(PermissionTypeFields.resource_fields, envelope='resource')
    def get(self):
        permission_types = PermissionType.query.all()
        return permission_types

    @swagger.operation(
        notes=u'Crea una nueva instancia de tipo de permiso, y la retorna.'.encode('utf-8'),
        responseClass='PermissionTypeFields',
        nickname='permissionTypeList_post',
        parameters=[
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
            },{
                "name": "can_edit_analysis_files",
                "description": (u'Permiso para editar los archivos del '
                                'análisis.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },{
                "name": "can_edit_measurements",
                "description": (u'Permiso para editar las mediciones del '
                                'análisis.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_201_created
        ]
    )
    @marshal_with(PermissionTypeFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_permission_type = PermissionType(args['name'],
                                             args['description'],
                                             args['can_view_analysis_files'],
                                             args['can_view_measurements'],
                                             args['can_edit_analysis_files'],
                                             args['can_edit_measurements'],
                                             )
        db.session.add(new_permission_type)
        db.session.commit()
        return new_permission_type, 201
