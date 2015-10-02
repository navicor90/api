# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class Analysis(db.Model):
    # Attributes
    id          = db.Column(db.Integer, primary_key=True)
    datetime    = db.Column(db.DateTime)
    description = db.Column(db.String(255))
    # Foreign keys
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    profile = db.relationship('Profile',
                              backref=db.backref('analyses', lazy='dynamic'))


    def __init__(self, datetime, description, profile_id):
        self.datetime    = datetime
        self.description = description
        self.profile_id  = profile_id

    def __repr__(self):
        return '<Analysis: %r>' % self.id
