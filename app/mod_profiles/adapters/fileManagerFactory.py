# -*- coding: utf-8 -*-

from app.mod_profiles.adapters.dropboxAdapter import DropboxAdapter
from app.mod_profiles.adapters.localAdapter import LocalAdapter


class FileManagerFactory(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FileManagerFactory, cls).__new__(cls, *args,
            **kwargs)
        return cls._instance

    def get_file_manager(self, name):
        """Ésta es una primera versión, integrando StorageCredentials y demás clases
        la búsqueda consistiría en buscar los StorageCredentials, de ahí ver si alguno
        está activo, en cuyo caso se obtiene de éste el storage location que determina
        el medio de almacenamiento externo a YesDoc. Si no encuentra ninguno activo,
        almacena en la ubicación de YesDoc.
        :param: Recibiría el User que está relacionado con el StorageLocation
        :return: DropboxAdapter or LocalAdapter
        """
        if name == 'Dropbox':
            return DropboxAdapter('prueba_drop')
        elif name == 'Local':
            return LocalAdapter('prueba_local')
