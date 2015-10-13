# -*- coding: utf-8 -*-

from StringIO import StringIO
from flask import g, send_file
from flask.ext.restful import Resource

from app.mod_shared.models.auth import auth
from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from app.mod_profiles.models import AnalysisFile


class AnalysisFileDownload(Resource):

    @auth.login_required
    def get(self, id):
        analysis_file = AnalysisFile.query.get_or_404(id)
        file_path = analysis_file.path
        file_name = file_path.rsplit('/')[-1]
        user = g.user
        file_manager = FileManagerFactory().get_file_manager(user)
        file_str = file_manager.download_file(file_path)
        str_in_out = StringIO()
        str_in_out.write(file_str)
        str_in_out.seek(0)
        return send_file(str_in_out, attachment_filename=file_name, as_attachment=True)
