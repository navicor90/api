# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class AnalysisFileEncryption(db.Model):
    # Attributes
    id                   = db.Column(db.Integer, primary_key=True)
    encrypted_secret_key = db.Column(db.Text)
    # Foreign keys
    analysis_file_id = db.Column(db.Integer, db.ForeignKey('analysis_file.id'))
    profile_id       = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    analysis_file = db.relationship('AnalysisFile',
                                    backref=db.backref('analysis_file_encryptions',
                                                       lazy='dynamic',
                                                       cascade='all, delete-orphan',
                                                       )
                                    )
    profile       = db.relationship('Profile',
                                    backref=db.backref('analysis_file_encryptions', lazy='dynamic'))

    def __init__(self, encrypted_secret_key, analysis_file_id, profile_id):
        self.encrypted_secret_key = encrypted_secret_key
        self.analysis_file_id     = analysis_file_id
        self.profile_id           = profile_id

    def __repr__(self):
        return '<AnalysisFileEncryption: %r>' % self.id
