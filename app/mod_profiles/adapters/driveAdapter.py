# -*- coding: utf-8 -*-

from oauth2client.client import AccessTokenCredentials
from werkzeug import secure_filename
from googleapiclient import errors
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
import httplib2



class DriveAdapter(object):
    def __init__(self, token):
        self.token = token

    def get_service(self):
        """
        :return: servicio de drive
        """
        credentials = AccessTokenCredentials(self.token, None)
        http = httplib2.Http()
        http = credentials.authorize(http)
        return build('drive', 'v2', http)

    def get_folder_id(self, folder_name, drive_service):
        """
        :param folder_name: nombre de la carpeta
        :param drive_service: servicio de drive
        :return: id de la carpeta en drive
        """
        param = {}
        param['q'] = "title = '{0}' and mimeType = 'application/vnd.google-apps.folder'".format(folder_name)
        try:
            folder_metadata = drive_service.files().list(**param).execute()
            folder_id = folder_metadata['items'][0]['id']
        except (errors.HttpError, IndexError), error:
            print 'Error en la carga a drive: %s' % error
            folder_id = None
        return folder_id

    def get_file_id(self, file_name, folder_id, drive_service):
        """
        :param file_name: nombre del archivo
        :param folder_id: id de la carpeta en drive
        :param drive_service: servicio de drive
        :return: id del archivo en drive
        """
        param = {}
        param['q'] = "title = '{0}'".format(file_name)
        try:
            children_metadata = drive_service.children().list(folderId=folder_id, **param).execute()
            file_id = children_metadata['items'][0]['id']
        except (errors.HttpError, IndexError), error:
            print 'Error en la carga a drive: %s' % error
            file_id = None
        return file_id

    def upload_file(self, img_file):
        """
        Carga un archivo en la cuenta de drive
        :param img_file: archivo
        :return: diccionario que indica la ruta del archivo, descripción y la ubicación de
        almacenamiento
        """
        folder_name = 'YesDoc'
        filename = secure_filename(img_file.filename)
        drive_service = self.get_service()
        try:
            # Obtengo el id de la carpeta YesDoc en drive
            folder_id = self.get_folder_id(folder_name, drive_service)
            # Compruebo que me devuelva un id para la carpeta
            # Si no la encuentra, creo la carpeta YesDoc en el directorio raíz
            if folder_id is None:
                body = {
                    'title': 'YesDoc',
                    'description': 'Carpeta de YesDoc: Asistente médico personal.',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                yesdoc_folder = drive_service.files().insert(body=body).execute()
                folder_id = yesdoc_folder['id']
            media = MediaIoBaseUpload(img_file, chunksize=1024 * 1024, mimetype='image/png', resumable=True)
            body = {
                'title': filename,
                'description': 'Imagen cargada a drive',
                "parents": [{
                    "kind": "drive#fileLink",
                    "id": folder_id
                }],
                'mimeType': 'image/png'
            }
            # Cargo el archivo a la carpeta YesDoc
            drive_service.files().insert(media_body=media, body=body).execute()
        except errors.HttpError, error:
            print 'Error en la carga a drive: %s' % error
            return None
        # Armo la respuesta para con los datos para AnalysisFile
        res = {
            'path': '/'+folder_name+'/'+filename,
            'description': 'Carga del archivo {0} en Drive'.format(folder_name),
            'storage_location': 'Dirve'
        }
        return res

    def download_file(self, path):
        """
        Descarga un archivo
        :param path: ruta del archivo en drive
        :return: archivo
        """
        path_list = path.split('/')
        # Obtengo de la ruta el nombre de la carpeta que contiene el archivo
        folder_name = path_list[len(path_list)-2]
        # Obtengo de la ruta el nombre del archivo
        file_name = path_list[len(path_list)-1]
        drive_service = self.get_service()
        folder_id = self.get_folder_id(folder_name, drive_service)
        file_id = self.get_file_id(file_name, folder_id, drive_service)
        try:
            # Descargo la imágen de drive
            img_file = drive_service.files().get_media(fileId=file_id).execute()
        except errors.HttpError, error:
            print 'Error en la carga a drive: %s' % error
            img_file = None
        return img_file

    def delete_file(self, path):
        """
        Elimina el archivo
        :param path: ruta del archivo en drive
        :return: nombre del archivo
        """
        path_list = path.split('/')
        folder_name = path_list[len(path_list)-2]
        file_name = path_list[len(path_list)-1]
        drive_service = self.get_service()
        folder_id = self.get_folder_id(folder_name, drive_service)
        file_id = self.get_file_id(file_name, folder_id, drive_service)
        try:
            drive_service.files().delete(fileId=file_id).execute()
            response = file_name
        except errors.HttpError, error:
            print 'Error en la carga a drive: %s' % error
            response = None
        return response


    def get_thumbnail(self, path):
        """
        Devuelve la vista previa de un archivo
        :param path: ruta del archivo en drive
        :return: imágen de vista previa
        """
        path_list = path.split('/')
        folder_name = path_list[len(path_list)-2]
        file_name = path_list[len(path_list)-1]
        drive_service = self.get_service()
        folder_id = self.get_folder_id(folder_name, drive_service)
        file_id = self.get_file_id(file_name, folder_id, drive_service)
        try:
            img_file_metadata = drive_service.files().get(fileId=file_id).execute()
            download_url = img_file_metadata['thumbnailLink']
            resp, content = drive_service._http.request(download_url)
        except errors.HttpError, error:
            print 'Error en la carga a drive: %s' % error
            content = None
        return content
