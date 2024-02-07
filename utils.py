import gspread
import google.auth
from gspread.exceptions import SpreadsheetNotFound
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


def verify_sheet(page: int, key: str):
    """
    return: is sliced ​​to remove the header and return only the data
    """
    try:
        ws = worksheet(key, page)

    except SpreadsheetNotFound as _:
        raise WorksheetException(
            f"\nSheet não encontrado! Verifique se a key está correta <{key}>\n"
        )

    values_list = ws.get_values()

    if not values_list:
        raise WorksheetException(f"Dados não encontrados!")

    return values_list[1:]
