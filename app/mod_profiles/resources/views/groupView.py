# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Group
from app.mod_profiles.common.fields.groupFields import GroupFields
from app.mod_profiles.common.parsers.group import parser_put
from app.mod_profiles.common.persistence import group as group_persistence
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_204_deleted, code_401, code_403, code_404


class GroupView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de grupo.'.encode('utf-8'),
        responseClass='GroupFields',
        nickname='groupView_get',
        parameters=[
            {
                "name": "group_id",
                "description": u'Identificador único del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_200_found,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupFields.resource_fields, envelope='resource')
    def get(self, group_id):
        # Obtiene el grupo.
        group = Group.query.get_or_404(group_id)

        # Verifica que el usuario autenticado sea miembro del grupo.
        if not group_persistence.is_group_member(group, g.user):
            return '', 403
        return group

    @swagger.operation(
        notes=u'Actualiza una instancia específica de grupo, y la retorna.'.encode('utf-8'),
        responseClass='GroupFields',
        nickname='groupView_put',
        parameters=[
            {
                "name": "group_id",
                "description": u'Identificador único del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "name",
                "description": u'Nombre del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "description",
                "description": u'Descripción del grupo.'.encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_200_updated,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupFields.resource_fields, envelope='resource')
    def put(self, group_id):
        # Obtiene el grupo.
        group = Group.query.get_or_404(group_id)

        # Verifica que el usuario autenticado sea administrador del grupo.
        if not group_persistence.is_group_admin(group, g.user):
            return '', 403

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        name = args['name']
        description = args['description']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificada.
        if (name is not None and
                group.name != name):
            group.name = name
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (description is not None and
                group.description != description):
            group.description = description

        db.session.commit()
        return group, 200

    @swagger.operation(
        notes=(u'Elimina una instancia específica de grupo, junto a todas sus '
               'membresías asociadas.').encode('utf-8'),
        nickname='groupView_delete',
        parameters=[
            {
                "name": "group_id",
                "description": u'Identificador único del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_204_deleted,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupFields.resource_fields, envelope='resource')
    def delete(self, group_id):
        # Obtiene el grupo.
        group = Group.query.get_or_404(group_id)

        # Verifica que el usuario autenticado sea administrador del grupo.
        if not group_persistence.is_group_admin(group, g.user):
            return '', 403

        # Elimina el grupo.
        db.session.delete(group)
        db.session.commit()

        return '', 204
