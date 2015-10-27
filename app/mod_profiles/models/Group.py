# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class Group(db.Model):
    # Attributes
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name        = name
        self.description = description

    def __repr__(self):
        return '<Group: %r>' % self.name
