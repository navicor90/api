# -*- coding: utf-8 -*-

import os
from flask import request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from app import app


# conjunto de extensiones de archivos permitidas
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg'])


# para evitar carga de archivos HTML que pueden causar problemas XSS
def allowed_file(filename):
    """Chequea si una extensión es válida
    :param filename: nombre del archivo
    :return Boolean
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # obtenemos el archivo del request
        file = request.files['file']
        if file and allowed_file(file.filename):
            # secure_filename se encarga de asegurar el archivo antes de almacenarlo en el filesystem.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload file</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
        <p><input type='file' name='image_file'>
        Usuario: <input type="number" name="user_id">
        Análisis: <input type="number" name="analysis_id">
        <input type='submit' value='Upload'>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # send_from_directory sirve el archivo cargado
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
