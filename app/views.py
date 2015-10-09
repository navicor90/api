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
