from __future__ import print_function

import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import data


# If modifying these scopes, delete the file token.json.

class table:

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'keys.json'
        self.SPREADSHEET_ID = '1oba360gqYTp2QFqMIgLwzE4VHiYJr-1VPXpwHtIJ488'

        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        self.service = build('sheets', 'v4', credentials=self.credentials)

        self.sheets = self.service.spreadsheets()
        x = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range="A1:I2000").execute()
        rows = x.get('values', [])
        print(rows[0])

    def updateTable(self, col, message):
        request = self.sheets.values().update(spreadsheetId=self.SPREADSHEET_ID, range=str(col),
                                              valueInputOption="USER_ENTERED", body={"values": message})

        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": int(data.getData_without_increase()),
                            "endRowIndex": int(data.getData_without_increase()),
                            "startColumnIndex": 0,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": 1,
                                    "green": 0,
                                    "blue": 0
                                }
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor"
                    }
                }
            ]
        }
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID,
                                                body=batch_update_spreadsheet_request_body).execute()

        request.execute()

    def getTable(self, col):
        x = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range=str(col)).execute()
        return x


a = table()
