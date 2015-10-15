# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class Permission(db.Model):
    # Attributes
    id                      = db.Column(db.Integer, primary_key=True)
    # Foreign keys
    analysis_id        = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    permission_type_id = db.Column(db.Integer, db.ForeignKey('permission_type.id'))
    user_id            = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Relationships
    analysis        = db.relationship('Analysis',
                                      backref=db.backref('permissions', lazy='dynamic'))
    permission_type = db.relationship('PermissionType',
                                      backref=db.backref('permissions', lazy='dynamic'))
    user            = db.relationship('User',
                                      backref=db.backref('permissions', lazy='dynamic'))

    def __init__(self, analysis_id, permission_type_id, user_id):
        self.analysis_id        = analysis_id
        self.permission_type_id = permission_type_id
        self.user_id            = user_id

    def __repr__(self):
        return '<PermissionType: %r>' % self.id
