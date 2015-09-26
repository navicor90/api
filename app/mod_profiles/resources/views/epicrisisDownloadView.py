# -*- coding: utf-8 -*-

from flask_restful import Resource
from app.mod_profiles.models import Epicrisis
from flask import send_file
from app.config import Config

class EpicrisisDownloadView(Resource):

    def get(self, id):
        epicrisis = Epicrisis.query.get_or_404(id)
        path = Config.uploaded_photos.path(epicrisis.image_name)
        return send_file(path, as_attachment=True, mimetype='image/x-portable-anymap')

