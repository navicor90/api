# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import AnalysisComment
from app.mod_profiles.common.fields.analysisCommentFields import AnalysisCommentFields
from app.mod_profiles.common.parsers.analysisComment import parser_put_auth
from app.mod_profiles.common.persistence import permission
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_401, code_403, code_404


class AnalysisCommentView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de comentario de análisis.'.encode('utf-8'),
        responseClass='AnalysisCommentFields',
        nickname='analysisCommentView_get',
        parameters=[
            {
                "name": "analysis_comment_id",
                "description": u'Identificador único del comentario de análisis.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            }
        ],
        responseMessages=[
            code_200_found,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisCommentFields.resource_fields, envelope='resource')
    def get(self, analysis_comment_id):
        # Obtiene el comentario de análisis.
        analysis_comment = AnalysisComment.query.get_or_404(analysis_comment_id)

        # Verifica que el usuario autenticado tenga permiso para ver los
        # comentarios del análisis asociado.
        if not permission.get_permission_by_user(analysis_comment.analysis, g.user, 'view_comments'):
            return '', 403

        return analysis_comment

    @swagger.operation(
        notes=u'Actualiza una instancia específica de comentario de análisis, y la retorna.'.encode('utf-8'),
        responseClass='AnalysisCommentFields',
        nickname='analysisCommentView_put',
        parameters=[
            {
                "name": "analysis_comment_id",
                "description": u'Identificador único del comentario de análisis.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "comment",
                "description": u'Contenido del comentario.'.encode('utf-8'),
                "required": True,
                "dataType": "string",
                "paramType": "body"
            }
        ],
        responseMessages=[
            code_200_updated,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisCommentFields.resource_fields, envelope='resource')
    def put(self, analysis_comment_id):
        # Obtiene el comentario de análisis.
        analysis_comment = AnalysisComment.query.get_or_404(analysis_comment_id)

        # Verifica que el usuario autenticado sea el dueño del comentario de
        # análisis especificado.
        if g.user.id != analysis_comment.profile.user.first().id:
            return '', 403

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put_auth.parse_args()
        comment = args['comment']

        # Actualiza los atributos del objeto, en base a los argumentos
        # recibidos.

        # Actualiza el contenido del comentario, en caso de que haya sido
        # modificado.
        if (comment is not None and
              analysis_comment.comment != comment):
            analysis_comment.comment = comment

        db.session.commit()
        return analysis_comment, 200
