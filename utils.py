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
