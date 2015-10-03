# -*- coding: utf-8 -*-

from flask.helpers import flash
from app.mod_shared.models.db import db
from app.mod_profiles.models import Epicrisis
from app.config import Config
from flaskext.uploads import UploadNotAllowed
# from werkzeug import secure_filename
# deberíamos usarlo para asegurar el nombre del archivo

class LocalAdapter(object):
    def __init__(self, name):
        self.name = name

    def upload_file(self, img_file, date_time):
        """File upload using Flask-Uploads
        """
        print date_time, type(date_time)
        try:
            image_name = Config.uploaded_photos.save(img_file)
            print image_name
        except UploadNotAllowed:
            # Tendría que ser reemplazado por un response adecuado
            flash("El archivo presenta un formato incorrecto")
        else:
            new_epicrisis = Epicrisis(image_name, date_time)
            db.session.add(new_epicrisis)
            db.session.commit()
            return new_epicrisis
