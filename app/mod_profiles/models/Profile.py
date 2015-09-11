# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db

class Profile(db.Model):
    # Attributes
    id         = db.Column(db.Integer, primary_key=True)
    last_name  = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    gender     = db.Column(db.Integer)
    birthday   = db.Column(db.Date)
    # Foreign keys
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    # Relationships
    gender = db.relationship('Gender',
                             backref=db.backref('profiles', lazy='dynamic'))


    def __init__(self, last_name, first_name, birthday, gender_id):
        self.last_name  = last_name
        self.first_name = first_name
        self.birthday   = birthday
        self.gender_id  = gender_id

    def __repr__(self):
        return '<Profile: %r %r>' % (self.first_name, self.last_name)
