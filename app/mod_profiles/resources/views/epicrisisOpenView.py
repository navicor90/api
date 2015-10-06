# -*- coding: utf-8 -*-

from app.mod_profiles.models.Epicrisis import Epicrisis
from flask_restful import Resource
from flask import send_from_directory
from app.config import Config


class EpicrisisOpenView(Resource):

    def get(self, id):
        epicrisis = Epicrisis.query.get_or_404(id)
        return (Config.UPLOADED_PHOTOS_DEST, epicrisis.image_name)
