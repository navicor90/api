# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.models import Analysis
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_403, code_404


class AnalysisAnalysisFileList(Resource):
    # Crea una copia de los campos del modelo 'AnalysisFile'.
    resource_fields = AnalysisFileFields.resource_fields.copy()
    # Quita el análisis asociado de los campos del recurso.
    del resource_fields['analysis']

    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de archivos de '
               'análisis, asociados a un análisis específico.').encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisAnalysisFileList_get',
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

        # Obtiene todos los archivos de análisis asociados al análisis.
        analysis_files = analysis.analysis_files.all()
        return analysis_files
