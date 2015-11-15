# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class GroupPermission(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    # Foreign keys
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    group_id    = db.Column(db.Integer, db.ForeignKey('group.id'))
    # Relationships
    analysis = db.relationship('Analysis',
                               backref=db.backref('group_permissions',
                                                  lazy='dynamic',
                                                  cascade='all, delete-orphan',
                                                  )
                               )
    group    = db.relationship('Group',
                               backref=db.backref('group_permissions', lazy='dynamic'))

    def __init__(self, analysis_id, group_id):
        self.analysis_id = analysis_id
        self.group_id    = group_id

    def __repr__(self):
        return '<GroupPermission: %r>' % self.id
