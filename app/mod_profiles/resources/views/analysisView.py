# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Analysis
from app.mod_profiles.common.fields.analysisFields import AnalysisFields
from app.mod_profiles.common.parsers.analysis import parser_put
from app.mod_profiles.common.persistence import analysisFile
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_204_deleted, code_401, code_403, code_404


class AnalysisView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de análisis.'.encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='analysisView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del análisis.'.encode('utf-8'),
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
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def get(self, analysis_id):
        analysis = Analysis.query.get_or_404(analysis_id)
        return analysis

    @swagger.operation(
        notes=u'Actualiza una instancia específica de análisis, y la retorna.'.encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='analysisView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "datetime",
              "description": u'Fecha y hora del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "datetime",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "profile_id",
              "description": u'Identificador único del perfil asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
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
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def put(self, analysis_id):
        analysis = Analysis.query.get_or_404(analysis_id)
        args = parser_put.parse_args()

        # Verifica que el usuario autenticado sea el dueño del análisis
        # especificado.
        if g.user.id != analysis.profile.user.first().id:
            return '', 403

        # Actualiza los atributos del objeto, en base a los argumentos
        # recibidos.

        # Actualiza la fecha y hora del análisis, en caso de que haya sido
        # modificado.
        if (args['datetime'] is not None and
              analysis.datetime != args['datetime']):
            analysis.datetime = args['datetime']
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (args['description'] is not None and
              analysis.description != args['description']):
            analysis.description = args['description']
        # Actualiza el perfil asociado, en caso de que haya sido modificado.
        if (args['profile_id'] is not None and
              analysis.profile_id != args['profile_id']):
            analysis.profile_id = args['profile_id']

        db.session.commit()
        return analysis, 200

    @swagger.operation(
        notes=(u'Elimina una instancia específica de análisis, junto a sus '
               'mediciones y archivos de análisis asociados.').encode('utf-8'),
        nickname='analysisView_delete',
        parameters=[
            {
                "name": "id",
                "description": u'Identificador único del análisis.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            }
        ],
        responseMessages=[
            code_204_deleted,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def delete(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario autenticado sea el dueño del archivo de
        # análisis especificado.
        if g.user.id != analysis.profile.user.first().id:
            return '', 403

        # Elimina todas las mediciones asociadas al análisis.
        measurements = analysis.measurements.all()
        for measurement in measurements:
            db.session.delete(measurement)

        # Elimina todos los archivos de análisis asociados al análisis.
        analysis_files = analysis.analysis_files.all()
        for analysis_file in analysis_files:
            # Elimina el archivo asociado de la ubicación de almacenamiento.
            analysisFile.delete_file(analysis_file)
            db.session.delete(analysis_file)

        # Elimina el análisis.
        db.session.delete(analysis)
        db.session.commit()

        return '', 204
