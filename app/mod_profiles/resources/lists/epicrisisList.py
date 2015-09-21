# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from app.mod_shared.models.db import db
from app.mod_profiles.models import Epicrisis
from app.mod_profiles.resources.fields.epicrisisFields import EpicrisisFields
from app.mod_profiles.common.parsers.epicrisis import parser_post
from app import config
import os


class EpicrisisList(Resource):

    def get(self):
        pass

    @marshal_with(EpicrisisFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        image = args['image']
        if image:
            name = image.filename.rsplit('.', 1)[0]
            image_source_dir = os.path.join(config['UPLOAD_FOLDER'],args['image'])
        new_gender = Epicrisis(args['datetime'],
                            args['description'])
        db.session.add(new_gender)
        db.session.commit()
        return new_gender, 201
