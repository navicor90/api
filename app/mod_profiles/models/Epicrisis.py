# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db

class Epicrisis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(50))
    datetime = db.Column(db.DateTime)

    def __init__(self, image_name, datetime):
        self.image_name = image_name
        self.datetime = datetime

