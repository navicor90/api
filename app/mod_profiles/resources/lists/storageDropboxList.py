# -*- coding: utf-8 -*-
from app.mod_profiles.common.parsers.storageDropboxList import parser
from app.mod_profiles.models.StorageCredentialsSC import StorageCredentialsSC
from app.mod_profiles.resources.fields.storageCredentialsSCFields import StorageCredentialsSCFields
from app.mod_shared.models.db import db
from dropbox.client import DropboxOAuth2Flow
from flask.ext.restful import Resource, marshal_with
from app.config import Config


class StorageDropboxList(Resource):

    @marshal_with(StorageCredentialsSCFields.resource_fields, envelope='resource')
    def get(self):
        args = parser.parse_args()
        dropboxOauth = DropboxOAuth2Flow(Config.app_key, Config.app_secret, "dropbox-auth-csrf-token")
        try:
            access_token, user_id, url_state = \
                dropboxOauth.finish(args['dropboxOauthTuple'])
            new_storage_credentials_sc = StorageCredentialsSC(access_token, True)
            db.session.add(new_storage_credentials_sc)
            db.session.commit()
            return new_storage_credentials_sc
        except DropboxOAuth2Flow.BadRequestException, e:
            #http_status(400)
            print "BadRequestException"
        except DropboxOAuth2Flow.BadStateException, e:
            # Start the auth flow again.
            #redirect_to("/dropbox-auth-start")
            print e.message
        except DropboxOAuth2Flow.CsrfException, e:
            #http_status(403)
            print e.message
        except DropboxOAuth2Flow.NotApprovedException, e:
            """
            flash('Not approved?  Why not?')
            return redirect_to("/home")
            """
            print e.message
        except DropboxOAuth2Flow.ProviderException, e:
            """
            logger.log("Auth error: %s" % (e,))
            http_status(403)
            """
            print e.message

