# -*- coding: utf-8 -*-

from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

class DriveAdapter(object):
    def __init__(self, token):
        self.token = "ya29.GQIx7l98FifvTMocfUNxiziS9J44V_IsbgJHsMxfcDOQHF5JxRsNepsXordRYj6L3Z6r"

    def upload_file(self, img_file):
        media = MediaFileUpload(img_file)
        drive_service = build('drive', 'v2', credentials=self.token)


    def download_file(self):
        pass

    def delete_file(self):
        pass

    def get_thumbnail(self):
        pass
