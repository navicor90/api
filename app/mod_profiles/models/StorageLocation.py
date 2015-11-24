# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class StorageLocation(db.Model):
    # Attributes
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    website     = db.Column(db.String(50))

    def __init__(self, name='', description='', website=''):
        self.name        = name
        self.description = description
        self.website     = website

    def __repr__(self):
        return '<StorageLocation: %r>' % self.name
