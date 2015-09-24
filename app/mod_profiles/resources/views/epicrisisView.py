# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask import send_from_directory, safe_join
from app.mod_profiles.models import Epicrisis
from app import config
from app.config import Config
from app.mod_profiles.resources.fields.epicrisisFields import EpicrisisFields
from flask import render_template


class EpicrisisView(Resource):

    #@marshal_with(EpicrisisFields.resource_fields, envelope='resource')
    def get(self, id):
        epicrisis = Epicrisis.query.get_or_404(id)
        print "Epicrisis: ", epicrisis
        print "config: {0} \n type_config: {1}".format(config, type(config))
        path = epicrisis.image_source_dir
        print "path ", path
        func = lambda x, y: x[y]
        filename = func(path.split('/'), len(path.split('/')) - 1)
        #filename = safe_join(Config.UPLOAD_FOLDER, filename)
        print "filename ", filename
        #return send_from_directory('/tmp', filename)
        return epicrisis


    def put(self):
        pass

    def remove(self):
        pass
