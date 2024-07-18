import os

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from config.models import Config


class StorageService:

    def __init__(self):

        SCOPES = ['https://www.googleapis.com/auth/drive']

        # Create credentials object
        creds = service_account.Credentials.from_service_account_info({
            'type': 'service_account',
            'client_email': os.getenv('CLIENT_EMAIL_GOOGLE'),
            'private_key': os.getenv('PRIVATE_KEY_GOOGLE'),
            'token_uri': 'https://oauth2.googleapis.com/token'
        }, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=creds)
        creds.refresh(Request())

    def set_file_permissions(self, file_id):
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()

    def upload_image(self, file_path, file_name, folder_id=None):

        file_metadata = {'name': file_name}

        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path, resumable=True)

        # Upload the file
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')

        self.set_file_permissions(file_id)

        return file_id

    def create_folder(self, folder_name, parent_folder_id=None):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]

        folder = self.service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        Config.add_config_value('GOOGLE_DRIVE_FOLDERS', folder_name, folder_id)

        self.set_folder_permissions(folder_id)

        return folder_id

    def set_folder_permissions(self, folder_id):
        permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': "lha657889@gmail.com"
        }

        self.service.permissions().create(
            fileId=folder_id,
            body=permission
        ).execute()
