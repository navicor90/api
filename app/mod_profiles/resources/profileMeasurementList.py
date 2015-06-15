from flask_restful import Resource, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementView import MeasurementView

class ProfileMeasurementList(Resource):
    # Crea una copia de los campos del recurso 'MeasurementView'.
    resource_fields = MeasurementView.resource_fields.copy()
    # Quita el perfil asociado de los campos del recurso.
    del resource_fields['profile']

    @marshal_with(resource_fields, envelope='resource')
    def get(self, profile_id):
        profile = Profile.query.get_or_404(profile_id)
        measurements = profile.measurements.all()
        return measurements