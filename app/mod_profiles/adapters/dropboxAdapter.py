# -*- coding: utf-8 -*-

from dropbox import dropbox, exceptions
from dropbox.files import FileMetadata, FolderMetadata, WriteMode

class DropboxAdapter(object):
    def __init__(self, name):
        self.name = name
    """
    Debería buscar el StorageCredential activo y pedirle que cargue el archivo
    que le paso como parámeto.
    """
    def upload_file(self, img_file, date_time):
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
        dbx = dropbox.Dropbox('')
        mode = WriteMode.add
        print type(img_file)
        print type(date_time)
        try:
            res = dbx.files_upload(img_file.read(), "/"+img_file.filename, mode, autorename=True)
            print res
        except exceptions.ApiError as err:
            print "Error en la carga. ", err.message
