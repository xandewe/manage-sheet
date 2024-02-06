from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("SHEET_NU_EXTRATO")
url = os.getenv("URL")
csv_path = os.getenv("SAVE_CSV_PATH")

CASA = ["COMPANHIA PAULISTA DE FORCA E LUZ", "CLARO", ]
TRANSPORTE = ["UBER"]
ALIMENTACAO = ["TAUSTE", "SWIFT", "KAWAKAMI", "IFOOD"]
