# -*- coding: utf-8 -*-

from flask_restful import Resource

from app.config import Config
from app.mod_profiles.models import Epicrisis


class EpicrisisOpenView(Resource):

    def get(self, id):
        epicrisis = Epicrisis.query.get_or_404(id)
        return (Config.UPLOADED_PHOTOS_DEST, epicrisis.image_name)
