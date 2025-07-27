import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "Bug Reports_Discord_Bot"

def get_sheet():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CREDENTIALS_PATH = os.path.join(BASE_DIR, "..", "secrets", "credentials.json")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    gc = gspread.authorize(credentials)
    return gc.open(SHEET_NAME).sheet1

def append_to_sheet(data_dict):
    try:
        sheet = get_sheet()
        headers = sheet.row_values(1)

        if not headers:
            headers = list(data_dict.keys())
            sheet.append_row(headers)

        values = [data_dict.get(key, "") for key in headers]
        sheet.append_row(values)

        print("✅ 구글 시트 저장 완료")
    except Exception as e:
        print(f"❌ 구글 시트 저장 오류: {e}")
