from gspread.worksheet import Worksheet
from gspread_formatting import (
    CellFormat as cell_format,
    Color as color,
    format_cell_range,
)
from decimal import Decimal, localcontext


def convert_values_sheet(ws: Worksheet):
    values_list = ws.col_values(2)
    line = 2

    for item in values_list[1:]:
        convert_number = float(item)
        ws.update_cell(line, 2, convert_number)


def write_sheet_headers(ws: Worksheet):

    ws.update_cell(1, 5, "Sub Tag")
    ws.update_cell(1, 6, "Tag")
    ws.update_cell(1, 7, "Entrada")
    ws.update_cell(1, 8, "Estorno/Reembolso")
    ws.update_cell(1, 9, "Resgate Invest.")
    ws.update_cell(1, 10, "Saida")
    ws.update_cell(1, 11, "Pagamento fatura credito")
    ws.update_cell(1, 12, "Investido")


def calculate_expense(ws: Worksheet, values_list: list):
    fmt = cell_format(backgroundColor=color(206 / 255, 76 / 255, 61 / 255))

    expense = 0
    invoice_card = 0
    invested = 0
    line = 2

    for item in values_list:
        date, value, id, description, *_ = item
        convert_number = Decimal(value)

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

    with localcontext() as ctx:
        ctx.prec = 10
        expense_convert = float(expense)
        invoice_card_convert = float(invoice_card)
        invested_convert = float(invested)

    ws.update_cell(2, 10, expense_convert)
    ws.update_cell(2, 11, invoice_card_convert)
    ws.update_cell(2, 12, invested_convert)


def calculate_income(ws: Worksheet, values_list: list):
    fmt = cell_format(backgroundColor=color(78 / 255, 127 / 255, 25 / 255))

    income = 0
    return_money = 0
    rescue = 0
    line = 2

    for item in values_list:
        date, value, id, description, *_ = item
        convert_number = Decimal(value)

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

    with localcontext() as ctx:
        ctx.prec = 10
        income_convert = float(income)
        return_money_convert = float(return_money)
        rescue_convert = float(rescue)

    ws.update_cell(2, 7, income_convert)
    ws.update_cell(2, 8, return_money_convert)
    ws.update_cell(2, 9, rescue_convert)
