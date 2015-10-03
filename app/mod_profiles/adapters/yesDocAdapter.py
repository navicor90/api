# -*- coding: utf-8 -*-

from flask.helpers import flash
import os
from app.config import Config
from flaskext.uploads import UploadNotAllowed
# from werkzeug import secure_filename
# deberíamos usarlo para asegurar el nombre del archivo


class YesDocAdapter(object):

    def upload_file(self, img_file, token=None):
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
            'description': 'Carga del archivo {0} en YesDoc'.format(fullname),
            'storage_location': 'YesDoc'
        }
        return res
