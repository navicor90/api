# -*- coding: utf-8 -*-

from dropbox import dropbox, exceptions
from dropbox.files import WriteMode


class DropboxAdapter(object):
    def __init__(self, token):
        self.token = token
    """
    Debería buscar el StorageCredential activo y pedirle que cargue el archivo
    que le paso como parámeto.
    """
    def upload_file(self, img_file):
        """
        Ya en el método creo una instancia del objeto DropboxClient pasandole
        como parámetro el token que obtengo del StorageCredential
        correspondiente. Puedo indicarle también un locale, que es el locale
        del user de nuestra aplicación, algunos llamados a la API retornan
        datos localizados y mensajes de error, ésta configuración le dice al
        server que locale usar (Por defecto en_US). También podemos indicarle
        un objeto cliente rest para usar para hacer requests.
        Para hacer una solicitud a la API de dropbox debemos armar un request
        específico. El método define la url objetivo ('/files')
        """
        dbx = dropbox.Dropbox(self.token)
        mode = WriteMode.add
        try:
            file_metadata = dbx.files_upload(img_file.read(), "/"+img_file.filename, mode, autorename=True)
        except exceptions.ApiError as err:
            print "Error en la carga a Dropbox ", err.message
            return None
        res = {
            'path': file_metadata.path_lower,
            'description': 'Carga del archivo {0} en Dropbox'.format(file_metadata.name),
            'storage_location': 'Dropbox'
        }
        return res

    def download_file(self, path):
        dbx = dropbox.Dropbox(self.token)
        try:
            fmd, res = dbx.files_download(path)
        except exceptions.HttpError as err:
            print '*** HTTP error', err.message
            return None
        return res.content
