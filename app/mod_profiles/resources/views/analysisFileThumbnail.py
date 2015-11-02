# -*- coding: utf-8 -*-

from StringIO import StringIO
from flask import g, send_file
from flask.ext.restful import Resource

from app.mod_shared.models.auth import auth
from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from app.mod_profiles.common.persistence import encryption, permission
from app.mod_profiles.models import AnalysisFile


class AnalysisFileThumbnail(Resource):

    @auth.login_required
    def get(self, analysis_file_id):
        analysis_file = AnalysisFile.query.get_or_404(analysis_file_id)

        # Verifica que el usuario autenticado tenga permiso para ver los
        # archivos de análisis, del análisis asociado.
        if not permission.get_permission_by_user(analysis_file.analysis, g.user, 'view_analysis_files'):
            return '', 403

        file_path = analysis_file.path
        file_name = file_path.rsplit('/')[-1]
        file_manager = FileManagerFactory().get_file_manager(g.user)

        # Verifica si el archivo de análisis está encriptado. De ser así,
        # recupera el archivo original. Sino, solicita su thumbnail a la
        # ubicación de almacenamiento.
        if analysis_file.is_encrypted:
            file_str = file_manager.download_file(file_path)
            # Obtiene la instancia de AnalysisFileEncryption, que fue generada
            # al encriptar el archivo.
            analysis_file_encryption = analysis_file.analysis_file_encryptions.first()
            # Obtiene la clave secreta encriptada.
            encrypted_secret_key = analysis_file_encryption.encrypted_secret_key
            # Obtiene la clave RSA privada del usuario que encriptó el archivo.
            rsa_private_key = analysis_file_encryption.profile.user.first().rsa_private_key
            # Desencripta la clave secreta con la clave RSA privada del usuario
            # que encriptó el archivo.
            secret_key = encryption.decrypt_secret_key(encrypted_secret_key,
                                                       rsa_private_key
                                                       )
            # Desencripta el archivo haciendo uso de la clave secreta.
            file_str = encryption.decrypt_file(file_str, secret_key)
        else:
            file_str = file_manager.get_thumbnail(file_path)

        str_in_out = StringIO()
        str_in_out.write(file_str)
        str_in_out.seek(0)
        return send_file(str_in_out, attachment_filename=file_name)
