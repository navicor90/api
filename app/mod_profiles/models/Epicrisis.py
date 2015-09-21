# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db

class Epicrisis(db.Model):
    id = db.column(db.Integer, primary_key = True)
    name = db.column(db.string(50))
    datetime = db.Column(db.DateTime)
    image_source_dir = db.column(db.string())

    def __init__(self, name, datetime, image_source_dir):
        self.name = name
        self.datetime = datetime
        self.image_source_dir = image_source_dir

