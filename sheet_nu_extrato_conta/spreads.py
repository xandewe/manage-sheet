from utils import worksheet
from . import key
from gspread.worksheet import Worksheet
from gspread_formatting import (
    CellFormat as cell_format,
    Color as color,
    format_cell_range,
)


def convert_values_sheet(ws: Worksheet):
    values_list = ws.col_values(2)
    line = 2

    for item in values_list[1:]:
        convert_number = float(item)
        ws.update_cell(line, 2, convert_number)


def calculate_expense(page=1):
    ws = worksheet(key, page)

    values_list = ws.get_values()

    if not values_list:
        print(f"Dados não encontrados!")
        return None

    fmt = cell_format(backgroundColor=color(206 / 255, 76 / 255, 61 / 255))

    ws.update_cell(1, 10, "Saida")
    ws.update_cell(1, 11, "Pagamento fatura credito")
    ws.update_cell(1, 12, "Investido")

    expense = 0
    invoice_card = 0
    invested = 0
    line = 2

    for item in values_list[1:]:
        date, value, id, description, *_ = item
        convert_number = float(value)

        if "aplicação rdb" in description.lower():
            invested += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        elif "pagamento de fatura" in description.lower():
            invoice_card += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        elif convert_number < 0:
            expense += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        line += 1

    ws.update_cell(2, 10, expense)
    ws.update_cell(2, 11, invoice_card)
    ws.update_cell(2, 12, invested)


def calculate_income(page=1):
    ws = worksheet(key, page)

    values_list = ws.get_values()

    if not values_list:
        print(f"Dados não encontrados!")
        return None

    fmt = cell_format(backgroundColor=color(78 / 255, 127 / 255, 25 / 255))

    ws.update_cell(1, 5, "Apelido")
    ws.update_cell(1, 6, "Tag")
    ws.update_cell(1, 7, "Entrada")
    ws.update_cell(1, 8, "Estorno/Reembolso")
    ws.update_cell(1, 9, "Resgate Invest.")

    income = 0
    return_money = 0
    rescue = 0
    line = 2

    for item in values_list[1:]:
        date, value, id, description, *_ = item
        convert_number = float(value)

        if (
            "estorno" in description.lower()
            or "reembolso recebido" in description.lower()
        ):
            return_money += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        elif "resgate" in description.lower():
            rescue += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        elif convert_number > 0:
            income += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        line += 1

    ws.update_cell(2, 7, income)
    ws.update_cell(2, 8, return_money)
    ws.update_cell(2, 9, rescue)
