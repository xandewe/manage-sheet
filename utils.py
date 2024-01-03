import gspread
from oauth2client.service_account import ServiceAccountCredentials


def worksheet(key, page=0):
    # Escopo utilizado
    scope = ["https://spreadsheets.google.com/feeds"]

    # Dados de autenticação
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    # Se autentica
    gc = gspread.authorize(credentials)

    # Abre a planilha
    wks = gc.open_by_key(key)

    # Para selecionar a planilha pelo o nome use o código abaixo
    # wks = gc.open('Teste Python')

    # Seleciona a primeira página da planilha
    worksheet = wks.get_worksheet(page)

    return worksheet


def create_template(key: str):
    scope = ["https://spreadsheets.google.com/feeds"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    gc = gspread.authorize(credentials)

    wks = gc.open_by_key(key)

    month_list = [
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

    for month in month_list:
        wks.add_worksheet(f"{month}_EXTRATO", 1000, 26)

    for month in month_list:
        wks.add_worksheet(f"{month}_CRED", 1000, 26)
