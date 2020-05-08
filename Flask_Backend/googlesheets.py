from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://spreadsheets.google.com/feeds']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1asF6NX19u4JtXCsb9cAIAec-S74Q1-qv4EWA78iFJuI'
SAMPLE_RANGE_NAME = 'Sheet8!A2:E'
SAMPLE_RANGE_NAME_DATA = 'record!A'
SAMPLE_RANGE_NAME_ACTION = 'record!B'
SAMPLE_RANGE_NAME_SCREEN = 'record!C'
SAMPLE_RANGE_NAME_GAMEOBJ = 'record!D'
SAMPLE_RANGE_NAME_TIMESTAMP = 'record!E'

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    '''
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
    '''
    return values

def read_data_for_range(sheetname):
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=sheetname + "!A2:C").execute()
    rows = result.get('values', [])
    print ('{0} rows retrieved.'.format(len(rows)))
    play_steps = {}
    j = 0
    for i in rows:
        element_type, x, y = "", "", ""
        action_from_sheet = i[1]
        if action_from_sheet == "click":
            step_data = i[0].rsplit("_", 3)
            y = step_data[2]
            x = step_data[1]
            element_type = step_data[0]
        if action_from_sheet == "action":
            element_type = i[0]

        screen = i[2]


        play_steps[j] = {
            "screen" : screen,
            "element_type"  : element_type,
            "x" : x,
            "y" : y,
            "action" : action_from_sheet
        }
        j+= 1
    return play_steps

def append(record_data):
    cell, data, action, screen, gameobj, timestamp = record_data
    service = build('sheets', 'v4', credentials=creds)
    values_timestamp = [
        [
                           timestamp
                       ],
    ]
    values_data = [
        [
            data
        ],
        # Additional rows ...
    ]

    values_action = [
        [
            action
        ],
    ]

    values_screen = [
        [
            screen
        ],
    ]
    values_gameobj = [
        [
          gameobj
        ],
    ]
    body = {
        'values': values_data
    }
    body_action = {
        'values': values_action
    }
    body_screen = {
        'values': values_screen
    }
    body_gameobj = {
        'values': values_gameobj
    }
    body_timestamp = {
        'values': values_timestamp
    }
    sheet = service.spreadsheets()
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_DATA + str(cell),
        valueInputOption="RAW", body=body).execute()
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_ACTION + str(cell),
        valueInputOption="RAW", body=body_action).execute()
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_SCREEN + str(cell),
        valueInputOption="RAW", body=body_screen).execute()
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_GAMEOBJ + str(cell),
        valueInputOption="RAW", body=body_gameobj).execute()
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_TIMESTAMP + str(cell),
        valueInputOption="RAW", body=body_timestamp).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))

def next_available_row(worksheet):
    str_list = filter(None, worksheet.col_values(1))
    return str(len(str_list)+1)

if __name__ == '__main__':
    main()