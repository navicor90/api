# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class AnalysisComment(db.Model):
    # Attributes
    id       = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    comment  = db.Column(db.UnicodeText)
    # Foreign keys
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    profile_id  = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    analysis = db.relationship('Analysis',
                               backref=db.backref('analysis_comments',
                                                  lazy='dynamic',
                                                  cascade='all, delete-orphan',
                                                  )
                               )
    profile  = db.relationship('Profile',
                               backref=db.backref('analysis_comments', lazy='dynamic'))

    def __init__(self, datetime, comment, analysis_id, profile_id):
        self.datetime    = datetime
        self.comment     = comment
        self.analysis_id = analysis_id
        self.profile_id  = profile_id

    def __repr__(self):
        return '<AnalysisComment: %r>' % self.id
