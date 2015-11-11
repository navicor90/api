# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class TypeUnitValidation(db.Model):
    # Attributes
    id        = db.Column(db.Integer, primary_key=True)
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    # Foreign keys
    measurement_type_id = db.Column(db.Integer, db.ForeignKey('measurement_type.id'))
    measurement_unit_id = db.Column(db.Integer, db.ForeignKey('measurement_unit.id'))
    # Relationships
    measurement_type = db.relationship('MeasurementType',
                                       backref=db.backref('validations', lazy='dynamic'))
    measurement_unit = db.relationship('MeasurementUnit',
                                       backref=db.backref('validations', lazy='dynamic'))

    def __init__(self, min_value, max_value, type_id, unit_id):
        self.min_value           = min_value
        self.max_value           = max_value
        self.measurement_type_id = type_id
        self.measurement_unit_id = unit_id

    def __repr__(self):
        return '<TypeUnitValidation: %r>' % self.id
