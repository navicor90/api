from flask_restful import Resource, reqparse, fields, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementSourceView import resource_fields as relation_measurement_source_fields
from .measurementTypeView import resource_fields as relation_measurement_type_fields
from .measurementUnitView import resource_fields as relation_measurement_unit_fields
from .profileView import resource_fields as relation_profile_fields


parser = reqparse.RequestParser()
parser.add_argument('datetime', required=True)
parser.add_argument('value', type=float, required=True)
parser.add_argument('profile_id', type=int, required=True)
parser.add_argument('measurement_source_id', type=int)
parser.add_argument('measurement_type_id', type=int, required=True)
parser.add_argument('measurement_unit_id', type=int, required=True)

resource_fields = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='iso8601'),
    'value': fields.Float,
    'profile': fields.Nested(relation_profile_fields),
    'measurement_source': fields.Nested(relation_measurement_source_fields),
    'measurement_type': fields.Nested(relation_measurement_type_fields),
    'measurement_unit': fields.Nested(relation_measurement_unit_fields),
}

class MeasurementView(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, id):
        measurement = Measurement.query.get_or_404(id)
        return measurement

    @marshal_with(resource_fields, envelope='resource')
    def put(self, id):
        measurement = Measurement.query.get_or_404(id)
        args = parser.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza la fecha y hora, en caso de que haya sido modificada.
        if (args['datetime'] is not None and
              measurement.datetime != args['datetime']):
            measurement.datetime = args['datetime']
        # Actualiza el valor, en caso de que haya sido modificado.
        if (args['value'] is not None and
              measurement.value != args['value']):
            measurement.value = args['value']
        # Actualiza el perfil asociado, en caso de que haya sido modificado.
        if (args['profile_id'] is not None and
              measurement.profile_id != args['profile_id']):
            measurement.profile_id = args['profile_id']
        # Actualiza la fuente de la medicion, en caso de que haya sido
        # modificada.
        if (args['measurement_source_id'] is not None and
              measurement.measurement_source_id != args['measurement_source_id']):
            measurement.measurement_source_id = args['measurement_source_id']
        # Actualiza el tipo de medicion, en caso de que haya sido modificado.
        if (args['measurement_type_id'] is not None and
              measurement.measurement_type_id != args['measurement_type_id']):
            measurement.measurement_type_id = args['measurement_type_id']
        # Actualiza la unidad de medida asociada, en caso de que haya sido
        # modificada.
        if (args['measurement_unit_id'] is not None and
              measurement.measurement_unit_id != args['measurement_unit_id']):
            measurement.measurement_unit_id = args['measurement_unit_id']

        db.session.commit()
        return measurement, 200