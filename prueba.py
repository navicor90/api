# -*- coding: utf-8 -*-

import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient import errors
from oauth2client.client import AccessTokenCredentials
import os
import flask
from flask import request, redirect, url_for
from werkzeug import secure_filename
import httplib2

from apiclient import discovery
from oauth2client import client


app = flask.Flask(__name__)


@app.route('/')
def index():
    print "FLASK SESSION before control", flask.session
    #print "FLASK SESSION CREDENTIALS", flask.session['credentials']
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    print "FLASK SESSION", flask.session
    print "CREDENTIALS", credentials
    print type(credentials)
    print "ACCESS TOKEN", credentials.access_token
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v2', http_auth)
        files = drive_service.files().list().execute()
        media = MediaFileUpload('/home/franco/prueba.txt', mimetype='text/plane', resumable=True)
        body = {
            'title': 'DocumentPrueba',
            'description': 'Imágen cargada a drive',
            'mimeType': 'text/plane'
        }
        file = drive_service.files().insert(
                    body=body,
                    media_body=media).execute()
    #return json.dumps(files)
    return file

@app.route('/oauth2callback')
def oauth2callback():

    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/drive.metadata.readonly',
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    flow.params['include_granted_scopes'] = 'true'
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))
    #return flask.redirect(flask.url_for('upload_file'))

@app.route('/uploads', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # obtenemos el archivo del request
        file = request.files['file']
        print "FILE", file.filename
        if file:
            # secure_filename se encarga de asegurar el archivo antes de almacenarlo en el filesystem.
            token = ''
            filename = secure_filename(file.filename)
            print "FILE NAME", filename
            print "FLASK SESSION on uploads", flask.session
            #credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
            credentials = AccessTokenCredentials(token, None)
            http = httplib2.Http()
            http = credentials.authorize(http)
            print "USER AGENT", credentials.user_agent
            http_auth = credentials.authorize(httplib2.Http())
            drive_service = build('drive', 'v2', http)
            print "DRIVE SERVICE", drive_service
            #print "TYPE FILE READED", type(f)
            media = MediaFileUpload('/home/franco/prueba.txt', mimetype='text/plane', resumable=True)
            body = {
                'title': 'DocumentPrueba',
                'description': 'Imágen cargada a drive',
                'mimeType': 'text/plane'
            }
            try:
                print "ENTRAAAAAA"
                file = drive_service.files().insert(
                    body=body,
                    media_body=media).execute()

                # Uncomment the following line to print the File ID
                # print 'File ID: %s' % file['id']

                return file
            except errors.HttpError, error:
                print 'An error occured: %s' % error
                return None
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="uploads" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''




if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = True
    app.run()