#  Взаимодействие с API гугл- таблиц и документов

# def get_tasks_from_gtable():
#     pass
#
#
# def get_post_content_from_gdoc():
#     pass
#
#
# def get_post_img():
#     pass

from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1fUgQWYFaqr8FuHIyJlrQp-ztrPpOugH9e0KJB6_aUSQ'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A2:I50',
    majorDimension='ROWS'
).execute()
pprint(values)
exit()
#
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {
#                 "range": "B3:C4",
#                 "majorDimension": "ROWS",
#                 "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]
#             },
#             {
#                 "range": "D5:E6",
#                 "majorDimension": "ROWS",
#                 "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]
#             }
#         ]
#     }
# ).execute()
