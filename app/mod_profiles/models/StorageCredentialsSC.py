# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db

class StorageCredentialsSC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    active = db.Column(db.Boolean)

    def __init__(self, token, active):
        self.token = token
        self.active = active
