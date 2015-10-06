# -*- coding: utf-8 -*-

from app.mod_profiles.adapters.dropboxAdapter import DropboxAdapter
from app.mod_profiles.adapters.yesDocAdapter import YesDocAdapter
from app.mod_profiles.models.StorageLocation import StorageLocation
from app.mod_profiles.common.persistence import storageCredential


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
        storage_credentials = storageCredential.get_by_user(user)
        storage_credential = None
        file_manager_name = None
        for sc in storage_credentials:
            if sc.token:
                storage_credential = sc
        if storage_credential is not None:
            storage_location = StorageLocation.query.get_or_404(storage_credential.storage_location_id)
            file_manager_name = storage_location.name
        if file_manager_name is not None and file_manager_name == 'Dropbox':
            return DropboxAdapter(storage_credential.token)
        else:
            return YesDocAdapter()
