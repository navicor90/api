# -*- coding: utf-8 -*-

import os

from app.mod_profiles.adapters import DropboxAdapter, YesDocAdapter, DriveAdapter


class FileManagerFactory(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FileManagerFactory, cls).__new__(cls, *args,
                                                                   **kwargs)
        return cls._instance

    def get_file_manager(self, user):
        """Ésta es una primera versión, integrando StorageCredentials y demás clases
        la búsqueda consistiría en buscar los StorageCredentials, de ahí ver si alguno
        está activo, en cuyo caso se obtiene de éste el storage location que determina
        el medio de almacenamiento externo a YesDoc. Si no encuentra ninguno activo,
        almacena en la ubicación de YesDoc.
        :param: Recibiría el User que está relacionado con el StorageLocation
        :return: DropboxAdapter or LocalAdapter
        """
        storage_credentials = user.storage_credentials
        storage_credential = None
        file_manager_name = None

        for sc in storage_credentials:
            if sc.token:
                storage_credential = sc
                break

        if storage_credential is not None:
            file_manager_name = storage_credential.storage_location.name
            token = storage_credential.token
        else:
            file_manager_name = 'Dropbox'
            token = os.environ.get('DROPBOX_STORAGE_TOKEN', '')

        if (file_manager_name is not None
                and token is not None):
            if file_manager_name == 'Dropbox':
                return DropboxAdapter(token)
            elif file_manager_name == 'Drive':
                return DriveAdapter(token)
        else:
            return YesDocAdapter()
