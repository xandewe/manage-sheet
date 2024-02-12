from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("SHEET_NU_EXTRATO")
url = os.getenv("URL")

SHEET_COLUMNS_NAME = (
    "Sub Tag",
    "Tag",
    "Total gasto",
    "Pagamento",
    "Desconto Ant.",
)

