# -*- coding: utf-8 -*-

import os
from flask.helpers import flash
from flaskext.uploads import UploadNotAllowed
# from werkzeug import secure_filename
# deberíamos usarlo para asegurar el nombre del archivo

from app.config import Config


class YesDocAdapter(object):

    def upload_file(self, img_file):
        """File upload using Flask-Uploads
        """
        try:
            fullname = Config.uploaded_photos.save(img_file)
        except UploadNotAllowed:
            # Tendría que ser reemplazado por un response adecuado
            flash("El archivo presenta un formato incorrecto")
            return None
        res = {
            'path': Config.UPLOADED_PHOTOS_DEST+os.path.sep+fullname,
            'description': 'Carga del archivo "{0}" en YesDoc'.format(fullname),
            'storage_location': 'YesDoc'
        }
        return res

    def download_file(self, path):
        var = open(path)
        return var.read()