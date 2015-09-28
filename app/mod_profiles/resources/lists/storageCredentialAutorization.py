# -*- coding: utf-8 -*-

from app.config import Config
from app.mod_profiles.common.parsers.storageCredentialAutorizationList import parser
from dropbox.client import DropboxOAuth2Flow
from flask_restful import Resource
from flask import redirect, url_for


class StorageCredentialAutorization(Resource):

    def post(self):
        args = parser.parse_args()
        redirect_uri = url_for('storage_dropbox', _external=True)
        authorize_url = \
            DropboxOAuth2Flow(Config.app_key, Config.app_secret, redirect_uri, "dropbox-auth-csrf-token").start()
        redirect(authorize_url)
