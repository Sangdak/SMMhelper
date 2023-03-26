from dotenv import load_dotenv
import os
import io
from pathlib import Path
import httplib2
from pprint import pprint

import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


load_dotenv()

CREDENTIALS_FILE: str = os.getenv('CREDENTIALS_FILE')
SPREADSHEET_ID: str = os.getenv('SPREADSHEET_ID')
IMG_FOLDER_ID: str = os.getenv('IMG_FOLDER_ID')
TEXT_FOLDER_ID: str = os.getenv('TEXT_FOLDER_ID')

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]
)

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_g_sheet_content() -> list[list]:
    """Получает список строк из гугл-таблицы (за исключением заголовка)"""
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A2:J50',
        majorDimension='ROWS'
    ).execute()
    # exit()
    return values['values']


def add_to_g_sheet(row_num: int, post_tg_link: str = 'Error', post_vk_link: str = 'Error'):
    """Добавляет в обрабатываемую строку таблицы информацию о размещённых постах (если она имеется)"""
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": f"J{row_num}",
                    "majorDimension": "ROWS",
                    "values": [["POSTED"]]
                },
                {
                    "range": f"H{row_num}",
                    "majorDimension": "ROWS",
                    "values": [[post_tg_link]]
                },
                {
                    "range": f"F{row_num}",
                    "majorDimension": "ROWS",
                    "values": [[post_vk_link]]
                },
            ]
        }
    ).execute()
    pprint(values)
    # exit()


def get_files_info_from_g_drive():
    """Получает информацию о всех сущностях, содержащихся на гугл-диске"""
    service = apiclient.discovery.build('drive', 'v3', credentials=credentials)
    results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name, mimeType, parents)",
    ).execute()

    images = {i['name']: i['id'] for i in results['files'] if i['mimeType'] == 'image/jpeg'}
    texts = {i['name']: i['id'] for i in results['files'] if i['mimeType'] == 'application/vnd.google-apps.document'}

    return images, texts


def download_img_from_g_drive(name, id, path='./imgs/') -> None:
    """Загружает изображение в соответствующую папку './imgs/' """
    service = apiclient.discovery.build('drive', 'v3', credentials=credentials)
    file_id = id
    request = service.files().get_media(fileId=file_id)
    filename = Path(path, name)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def download_txt_from_g_drive(name, id, path='./txts/') -> None:
    """Загружает текстовый файл в соответствующую папку './imgs/' """
    service = apiclient.discovery.build('drive', 'v3', credentials=credentials)
    file_id = id
    request = service.files().export_media(fileId=file_id, mimeType='text/plain')
    filename = Path(path, name)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def download_files_to_dirs():
    imgs, txts = get_files_info_from_g_drive()

    for k, v in imgs.items():
        download_img_from_g_drive(k, v)

    for k, v in txts.items():
        download_txt_from_g_drive(k, v)
