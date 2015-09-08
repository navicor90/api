# -*- coding: utf-8 -*-

from app.mod_shared.models import db

# Many-to-many relationship tables
measurement_units_table = db.Table('measurement_units_table',
                                   db.Column('measurement_unit_id',
                                             db.Integer,
                                             db.ForeignKey('measurement_unit.id')),
                                   db.Column('measurement_type_id',
                                             db.Integer,
                                             db.ForeignKey('measurement_type.id')),
                                   db.PrimaryKeyConstraint('measurement_unit_id',
                                                           'measurement_type_id')
                                  )

class MeasurementType(db.Model):
    # Attributes
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    # Relationships
    measurement_units = db.relationship('MeasurementUnit',
                                        secondary=measurement_units_table,
                                        backref=db.backref('measurement_types', lazy='dynamic'))

    def __init__(self, name, description):
        self.name        = name
        self.description = description

    def __repr__(self):
        return '<MeasurementType: %r>' % (self.name)
