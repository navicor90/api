# -*- coding: utf-8 -*-
from flask.helpers import flash

import os
from flask_restful import Resource, marshal_with
from app.mod_shared.models.db import db
from app.mod_profiles.models import Epicrisis
from app.mod_profiles.resources.fields.epicrisisFields import EpicrisisFields
from app.mod_profiles.common.parsers.epicrisis import parser_post
from app.config import Config
from werkzeug import secure_filename

from app.config import Config
from flaskext.uploads import UploadNotAllowed


class EpicrisisList(Resource):

    def get(self):
        pass

    @marshal_with(EpicrisisFields.resource_fields, envelope='resource')
    def post(self):
        """ Basic file upload
        args = parser_post.parse_args()
        image_file = args['image']
        print image_file.filename
        if image_file is not None:
            filename = secure_filename(image_file.filename)
            print filename
            name = filename.rsplit('.')[0]
            print name
            image_file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            print image_file_path
            image_file.save(image_file_path)
            new_epicrisis = Epicrisis(name, args['datetime'], image_file_path)
            print new_epicrisis.name
            db.session.add(new_epicrisis)
            db.session.commit()
            return new_epicrisis, 201
        """
        """File upload using Flask-Uploads
        """
        args = parser_post.parse_args()
        image_file = args['image']
        print image_file
        if not image_file:
            flash("Debe cargar un archivo")
        else:
            try:
                filename = Config.uploaded_photos.save(image_file)
                print filename
            except UploadNotAllowed:
                flash("El archivo presenta un formato incorrecto")
            else:
                new_epicrisis = Epicrisis('archivo', args['datetime'], filename)
                print new_epicrisis
                db.session.add(new_epicrisis)
                db.session.commit()
                return new_epicrisis, 201

