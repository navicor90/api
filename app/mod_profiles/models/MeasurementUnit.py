# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db

class MeasurementUnit(db.Model):
    # Attributes
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(50), unique=True)
    symbol = db.Column(db.String(10))
    suffix = db.Column(db.Boolean)
    

    def __init__(self, name, symbol, suffix):
        self.name   = name
        self.symbol = symbol
        self.suffix = suffix

    def __repr__(self):
        return '<MeasurementUnit: %r>' % (self.name)
