from utils import worksheet
from . import key
from gspread_formatting import (
    CellFormat as cell_format,
    Color as color,
    format_cell_range,
)


def calculate_expense_credit(page=1):
    ws = worksheet(key, page)

    values_list = ws.get_values()

    if not values_list:
        print(
            f"Dados não encontrados! (Verifique também se a sua variável de ambiente está correta em relação a planilha a ser manipulada)"
        )
        return None

    fmt = cell_format(backgroundColor=color(206 / 255, 76 / 255, 61 / 255))

    ws.update_cell(1, 5, "Sub Tag")
    ws.update_cell(1, 6, "Tag")
    ws.update_cell(1, 7, "Total gasto")

    expense_credit = 0
    line = 2

    for item in values_list[1:]:
        date, category, title, value, *_ = item
        convert_number = float(value)

        if convert_number > 0:
            expense_credit += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        line += 1

    ws.update_cell(2, 7, expense_credit)


def calculate_payment(page=1):
    ws = worksheet(key, page)

    values_list = ws.get_values()

    if not values_list:
        print(f"Dados não encontrados!")
        return None

    fmt = cell_format(backgroundColor=color(78 / 255, 127 / 255, 25 / 255))

    ws.update_cell(1, 8, "Pagamento")

    payment = 0
    line = 2

    for item in values_list[1:]:
        date, category, title, value, *_ = item
        convert_number = float(value)

        if convert_number < 0:
            payment += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt)

        line += 1

    ws.update_cell(2, 8, payment)
