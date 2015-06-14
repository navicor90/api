from flask_restful import Resource, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementView import resource_fields as measurement_fields

# Crea una copia de los campos del recurso 'Measurement'.
resource_fields = measurement_fields.copy()
# Quita el perfil asociado de los campos del recurso.
del resource_fields['profile']

class ProfileLatestMeasurementList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, profile_id):
        measurement_types = MeasurementType.query.all()
        profile = Profile.query.get_or_404(profile_id)
        measurements = profile.measurements
        latest_measurements = []

        for measurement_type in measurement_types:
            latest_from_type = None
            corresponding_measurements = measurements.filter_by(measurement_type_id = measurement_type.id)
            for measurement in corresponding_measurements:
                if (not latest_from_type or
                      measurement.datetime > latest_from_type.datetime):
                    latest_from_type = measurement
            if (latest_from_type):
                latest_measurements.append(latest_from_type)

        return latest_measurements