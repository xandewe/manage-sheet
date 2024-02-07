import gspread
import google.auth
from gspread.exceptions import SpreadsheetNotFound

# from sheet_nu_extrato_conta import key
from exceptions import WorksheetException
from sheet_nu_extrato_conta import MONTH_LIST


def worksheet(key, page=0):
    scope = ["https://spreadsheets.google.com/feeds"]

    credentials, _ = google.auth.default(scope)

    gc = gspread.authorize(credentials)

    wks = gc.open_by_key(key)

    worksheet = wks.get_worksheet(page)

    return worksheet


def create_template(key: str):
    scope = ["https://spreadsheets.google.com/feeds"]

    credentials, _ = google.auth.default(scope)

    gc = gspread.authorize(credentials)

    wks = gc.open_by_key(key)

    for month in MONTH_LIST:
        wks.add_worksheet(f"{month}_EXTRATO", 1000, 26)

    for month in MONTH_LIST:
        wks.add_worksheet(f"{month}_CRED", 1000, 26)
