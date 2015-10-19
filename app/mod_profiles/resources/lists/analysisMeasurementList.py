# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.models import Analysis
from app.mod_profiles.common.fields.measurementFields import MeasurementFields
from app.mod_profiles.common.persistence import permission
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_403, code_404


class AnalysisMeasurementList(Resource):
    # Crea una copia de los campos del modelo 'Measurement'.
    resource_fields = MeasurementFields.resource_fields.copy()
    # Quita el análisis asociado de los campos del recurso.
    del resource_fields['analysis']

    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de medición, '
               'asociadas a un análisis específico.').encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='analysisMeasurementList_get',
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

        # Verifica que el usuario autenticado tenga permiso para ver las
        # mediciones del análisis especificado.
        if not permission.get_permission_by_user(analysis, g.user, 'view_measurements'):
            return '', 403

        # Obtiene todas las mediciones asociadas al análisis.
        measurements = analysis.measurements.all()
        return measurements
