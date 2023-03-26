import requests
import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint
import io
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



def get_files_from_folder(folder_id):
    files = []
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        files.append({
            'id': item['id'],
            'name': item['name'],
            'mime_type': item['mimeType']
        })
    return files


def send_post_on_tg():
    # bot = telegram.Bot(token=bot_api_key)

    CREDENTIALS_FILE = 'creds.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        [
            'https://www.googleapis.com/auth/drive',
        ]
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    IMG_FOLDER_ID = '1ka9NV35hfbL2p8EZf6Xk9CsmNcp_YYmk'
    TEXT_FOLDER_ID = '12zqTfyWqtx758A3Im5z2Utn4OP43oVdm'

    text_file_path = get_files_from_folder(TEXT_FOLDER_ID)[0]['id']
    img_files = get_files_from_folder(IMG_FOLDER_ID)
    img_file_path = img_files[0]['id']

    img_response = service.files().get_media(fileId=img_file_path)
    img_bytes = io.BytesIO(img_response.execute())
    img = Image.open(img_bytes)

    with open(text_file_path, 'r') as f:
        text = f.read()

    bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=text)


if __name__ == "__main__":
    bot_api_key = '5903927146:AAEI3horMhwAGg0MPKsFtG2jXCdKPAPFADk'
    tg_chat_id = '1001815682844'
