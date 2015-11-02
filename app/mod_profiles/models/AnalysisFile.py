# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class AnalysisFile(db.Model):
    # Attributes
    id           = db.Column(db.Integer, primary_key=True)
    upload_time  = db.Column(db.DateTime)
    path         = db.Column(db.String(255))
    description  = db.Column(db.String(255))
    is_encrypted = db.Column(db.Boolean)
    # Foreign keys
    analysis_id         = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'))
    # Relationships
    analysis         = db.relationship('Analysis',
                                       backref=db.backref('analysis_files',
                                                          lazy='dynamic',
                                                          cascade='all, delete-orphan',
                                                          )
                                       )
    storage_location = db.relationship('StorageLocation',
                                       backref=db.backref('analysis_files', lazy='dynamic'))

    def __init__(self, upload_time, path, description, analysis_id, storage_location_id, is_encrypted):
        self.upload_time          = upload_time
        self.path                 = path
        self.description          = description
        self.analysis_id          = analysis_id
        self.storage_location_id  = storage_location_id
        self.is_encrypted         = is_encrypted

    def __repr__(self):
        return '<AnalysisFile: %r>' % self.id
