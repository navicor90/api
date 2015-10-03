# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import Analysis
from app.mod_profiles.common.fields.analysisFields import AnalysisFields
from app.mod_profiles.common.parsers.analysis import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created


class AnalysisList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de análisis.'.encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='analysisList_get',
        responseMessages=[
            code_200_ok
        ]
    )
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def get(self):
        analyses = Analysis.query.all()
        return analyses

    @swagger.operation(
        notes=u'Crea una nueva instancia de análisis, y la retorna.'.encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='analysisList_post',
        parameters=[
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
            code_201_created
        ]
    )
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_analysis = Analysis(args['datetime'],
                                args['description'],
                                args['profile_id'])
        db.session.add(new_analysis)
        db.session.commit()
        return new_analysis, 201
