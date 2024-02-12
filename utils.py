import gspread
import google.auth
from gspread.exceptions import SpreadsheetNotFound
from exceptions import WorksheetException
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

key = os.getenv("SHEET_NU_EXTRATO")
url = os.getenv("URL")
csv_path = os.getenv("SAVE_CSV_PATH")
standard_month = str(datetime.now().month)
standard_year = str(datetime.now().year)

CASA = [
    "COMPANHIA PAULISTA DE FORCA E LUZ",
    "CLARO",
]
TRANSPORTE = ["UBER"]
ALIMENTACAO = ["TAUSTE", "SWIFT", "KAWAKAMI", "IFOOD"]

MONTH_LIST = [
    "JAN",
    "FEV",
    "MAR",
    "ABR",
    "MAI",
    "JUN",
    "JUL",
    "AGO",
    "SET",
    "OUT",
    "NOV",
    "DEZ",
]
PACKAGE_PATH = "./package_csv"


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
    That function was created for make a connection with worksheet and return infos needs. How:

    ws = worksheet Instance

    values_list = worksheet infos wihout headers

    quantity_columns = numeric value the columns quantity

    return: is sliced ​​to remove the header and return only the data
    """
    try:
        ws = worksheet(key, page)
        quantity_columns = len(ws.row_values(1))

    except SpreadsheetNotFound as _:
        raise WorksheetException(
            f"\nSheet não encontrado! Verifique se a key está correta <{key}>\n"
        )

    values_list = ws.get_values()

    if not values_list:
        raise WorksheetException(f"Dados não encontrados!")

    return (ws, values_list[1:], quantity_columns)


def read_csv(file: str) -> pd.DataFrame:
    try:
        data_frame = pd.read_csv(file)
    except FileNotFoundError as _:
        raise FileNotFoundError(f"Arquivo {file} não encontrado")

    return data_frame
