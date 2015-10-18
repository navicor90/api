# -*- coding: utf-8 -*-

from datetime import datetime
from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Analysis, AnalysisComment
from app.mod_profiles.common.fields.analysisCommentFields import AnalysisCommentFields
from app.mod_profiles.common.parsers.analysisComment import parser_post_auth
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created, code_401, \
    code_403, code_404


class AnalysisAnalysisCommentList(Resource):
    # Crea una copia de los campos del modelo 'AnalysisComment'.
    resource_fields = AnalysisCommentFields.resource_fields.copy()
    # Quita el análisis asociado de los campos del recurso.
    del resource_fields['analysis']

    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de comentario de '
               'análisis, asociadas a un análisis específico, ordenados por '
               'fecha y hora del comentario.').encode('utf-8'),
        responseClass='AnalysisCommentFields',
        nickname='analysisCommentList_get',
        parameters=[
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_200_ok,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(resource_fields, envelope='resource')
    def get(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario autenticado sea el dueño del análisis
        # especificado.
        if g.user.id != analysis.profile.user.first().id:
            return '', 403

        # Obtiene todos los comentarios de análisis asociados al análisis, y
        # los ordena por fecha y hora.
        analysis_comments = analysis.analysis_comments.order_by(AnalysisComment.datetime).all()
        return analysis_comments

    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Crea una nueva instancia de comentario de análisis, asociada '
               'al perfil del usuario autenticado y al análisis especificado, '
               'y la retorna.').encode('utf-8'),
        responseClass='AnalysisCommentFields',
        nickname='analysisCommentList_post',
        parameters=[
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis.'.encode('utf-8'),
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
            code_201_created,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisCommentFields.resource_fields, envelope='resource')
    def post(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post_auth.parse_args()
        comment = args['comment']

        # Crea el nuevo comentario de análisis.
        new_analysis_comment = AnalysisComment(datetime.utcnow(),
                                               comment,
                                               analysis.id,
                                               g.user.profile.id)

        db.session.add(new_analysis_comment)
        db.session.commit()
        return new_analysis_comment, 201