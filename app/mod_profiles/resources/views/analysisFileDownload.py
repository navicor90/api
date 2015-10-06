# -*- coding: utf-8 -*-

import StringIO
from flask import send_file
from flask.ext.restful import Resource

from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from app.mod_profiles.models import AnalysisFile, User


class AnalysisFileDownload(Resource):

    def get(self, id):
        analysis_file = AnalysisFile.query.get_or_404(id)
        file_path = analysis_file.path
        file_name = file_path.rsplit('/')[-1]
        # harcodeo esto porque no entiendo todavía como usar los datos de
        # user en el objeto g, no se como probarlo desde el navegador.
        user = User.query.get_or_404(1)
        file_manager = FileManagerFactory().get_file_manager(user)
        file_str = file_manager.download_file(file_path)
        str_in_out = StringIO.StringIO()
        str_in_out.write(file_str)
        str_in_out.seek(0)
        return send_file(str_in_out, attachment_filename=file_name, as_attachment=True)
