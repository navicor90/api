# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class StorageCredential(db.Model):
    # Attributes
    id          = db.Column(db.Integer, primary_key=True)
    token       = db.Column(db.String(255))
    # Foreign keys
    owner_id            = db.Column(db.Integer, db.ForeignKey('user.id'))
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'))
    # Relationships
    owner            = db.relationship('User',
                                       backref=db.backref('storage_credentials', lazy='dynamic'))
    storage_location = db.relationship('StorageLocation',
                                       backref=db.backref('storage_credentials', lazy='dynamic'))

    def __init__(self, token, owner_id, storage_location_id):
        self.token               = token
        self.owner_id            = owner_id
        self.storage_location_id = storage_location_id

    def __repr__(self):
        return '<StorageCredential: %r>' % self.id
