from gspread.worksheet import Worksheet
from gspread_formatting import (
    CellFormat as cell_format,
    Color as color,
    format_cell_range,
)
from decimal import Decimal, localcontext
from . import SHEET_COLUMNS_NAME


def write_sheet_headers(ws: Worksheet, column: int):
    for item in SHEET_COLUMNS_NAME:
        column += 1
        ws.update_cell(1, column, item)


def cash_inflows_and_outflows_analysis(ws: Worksheet, values_list: list):
    fmt_cash_outflow = cell_format(backgroundColor=color(206 / 255, 76 / 255, 61 / 255))
    fmt_invoice_card = cell_format(backgroundColor=color(249 / 255, 123 / 255, 112 / 255))
    fmt_cash_inflow = cell_format(backgroundColor=color(78 / 255, 127 / 255, 25 / 255))

    income = 0
    return_money = 0
    rescue = 0
    expense = 0
    invoice_card = 0
    invested = 0
    line = 2

    for item in values_list:
        date, value, id, description, *_ = item
        convert_number = Decimal(value)

        if "aplicação rdb" in description.lower() and convert_number < 0:
            invested += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_outflow)

        elif "pagamento de fatura" in description.lower() and convert_number < 0:
            invoice_card += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_invoice_card)

        elif convert_number < 0:
            expense += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_outflow)

        if (
            "estorno" in description.lower()
            or "reembolso recebido" in description.lower()
            and convert_number > 0
        ):
            return_money += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_inflow)

        elif "resgate" in description.lower() and convert_number > 0:
            rescue += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_inflow)

        elif convert_number > 0:
            income += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_inflow)

        line += 1

    with localcontext() as ctx:
        ctx.prec = 10
        income_convert = float(income)
        return_money_convert = float(return_money)
        rescue_convert = float(rescue)
        expense_convert = float(expense)
        invoice_card_convert = float(invoice_card)
        invested_convert = float(invested)

    return (
        income_convert,
        return_money_convert,
        rescue_convert,
        expense_convert,
        invoice_card_convert,
        invested_convert,
    )


def write_values_in_sheet(ws: Worksheet, values: tuple):
    col = ws.find("Tag", in_row=1).col

    for item in values:
        col += 1
        ws.update_cell(2, col, item)
