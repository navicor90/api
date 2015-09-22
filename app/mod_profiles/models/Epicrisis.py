# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db

class Epicrisis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    datetime = db.Column(db.DateTime)
    image_source_dir = db.Column(db.String())

    def __init__(self, name, datetime, image_source_dir):
        self.name = name
        self.datetime = datetime
        self.image_source_dir = image_source_dir

