# -*- coding: utf-8 -*-

from datetime import datetime
from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from app.mod_profiles.models import Analysis, AnalysisFile, AnalysisFileEncryption, StorageLocation
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.common.parsers.analysisFile import parser_post
from app.mod_profiles.common.persistence import encryption, permission
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created, code_401, \
    code_403


class AnalysisFileList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de archivos de '
               'análisis.').encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileList_get',
        responseMessages=[
            code_200_ok
        ]
    )
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def get(self):
        analysis_files = AnalysisFile.query.all()
        return analysis_files

    @swagger.operation(
        notes=u'Crea una nueva instancia de archivo de análisis, y la retorna.'.encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileList_post',
        parameters=[
            {
                "name": "image_file",
                "description": u'Archivo de análisis.'.encode('utf-8'),
                "required": True,
                "dataType": "file",
                "paramType": "form"
            },
            {
                "name": "description",
                "description": u'Descripción del archivo de análisis.'.encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis asociado.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "is_encrypted",
                "description": (u'Variable booleana que indica si el archivo '
                               'debe ser encriptado. Por defecto, es falso.').encode('utf-8'),
                "required": False,
                "dataType": "boolean",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_201_created,
            code_401,
            code_403
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def post(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post.parse_args()
        image_file = args['image_file']
        description = args['description']
        is_encrypted = args['is_encrypted'] or False
        analysis_id = args['analysis_id']

        # Obtiene el análisis especificado.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario autenticado tenga permiso para editar los
        # archivos de análisis, del análisis especificado.
        if not permission.get_permission_by_user(analysis, g.user, 'edit_analysis_files'):
            return '', 403

        # Verifica si el archivo debe ser encriptado.
        if is_encrypted:
            # Verifica que el usuario autenticado tenga generado su par de
            # claves RSA.
            if (g.user.rsa_public_key is None or
                    g.user.rsa_public_key == ''):
                # Crea el par de claves RSA del usuario.
                g.user.create_rsa_keys()
                db.session.add(g.user)
                db.session.flush()
            # Genera una nueva clave secreta para encriptar el archivo.
            secret_key = encryption.generate_secret_key(32)
            # Encripta la clave secreta con la clave RSA pública del usuario autenticado.
            encrypted_secret_key = encryption.encrypt_secret_key(secret_key, g.user.rsa_public_key)
            # Encripta el archivo haciendo uso de la clave secreta.
            image_file = encryption.encrypt_file(image_file, secret_key)

        file_manager = FileManagerFactory().get_file_manager(analysis.profile.user.first())
        res = file_manager.upload_file(image_file)
        storage_location = StorageLocation.query.filter_by(name=res['storage_location']).first()
        if storage_location is None:
            raise ValueError("No se encuentra una ubicación con la denominación especificada.")

        new_analysis_file = AnalysisFile(datetime.utcnow(),
                                         res['path'],
                                         description,
                                         analysis.id,
                                         storage_location.id,
                                         is_encrypted
                                         )
        db.session.add(new_analysis_file)

        if is_encrypted:
            db.session.flush()
            new_analysis_file_encryption = AnalysisFileEncryption(encrypted_secret_key,
                                                                  new_analysis_file.id,
                                                                  g.user.profile.id
                                                                  )
            db.session.add(new_analysis_file_encryption)

        db.session.commit()
        return new_analysis_file, 201
