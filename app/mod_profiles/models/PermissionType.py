# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class PermissionType(db.Model):
    # Attributes
    id                      = db.Column(db.Integer, primary_key=True)
    name                    = db.Column(db.String(50))
    description             = db.Column(db.String(255))
    can_view_analysis_files = db.Column(db.Boolean)
    can_view_measurements   = db.Column(db.Boolean)
    can_edit_analysis_files = db.Column(db.Boolean)
    can_edit_measurements   = db.Column(db.Boolean)

    def __init__(self, name, description, can_view_analysis_files, can_view_measurements,
                 can_edit_analysis_files, can_edit_measurements):
        self.name                    = name
        self.description             = description
        self.can_view_analysis_files = can_view_analysis_files
        self.can_view_measurements   = can_view_measurements
        self.can_edit_analysis_files = can_edit_analysis_files
        self.can_edit_measurements   = can_edit_measurements

    def __repr__(self):
        return '<PermissionType: %r>' % self.name
