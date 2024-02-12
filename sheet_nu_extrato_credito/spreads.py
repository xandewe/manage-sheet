from utils import worksheet
from gspread.worksheet import Worksheet
from . import key, SHEET_COLUMNS_NAME
from gspread_formatting import (
    CellFormat as cell_format,
    Color as color,
    format_cell_range,
)
from decimal import Decimal, localcontext
from gspread.exceptions import SpreadsheetNotFound


def write_sheet_headers(ws: Worksheet, column: int):
    for item in SHEET_COLUMNS_NAME:
        column += 1
        ws.update_cell(1, column, item)


def cash_inflows_and_outflows_analysis(ws: Worksheet, values_list: list):
    fmt_cash_outflow = cell_format(backgroundColor=color(206 / 255, 76 / 255, 61 / 255))
    fmt_cash_inflow = cell_format(backgroundColor=color(78 / 255, 127 / 255, 25 / 255))

    expense_credit = 0
    payment = 0
    discount = 0
    line = 2

    for item in values_list:
        date, category, title, value, *_ = item
        convert_number = Decimal(value)

        if convert_number > 0:
            expense_credit += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_outflow)

        if "discount" in category and convert_number < 0:
            discount += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_inflow)

        elif convert_number < 0:
            payment += convert_number
            format_cell_range(ws, f"A{line}:D{line}", fmt_cash_inflow)

        line += 1

    with localcontext() as ctx:
        ctx.prec = 10
        expense_credit_convert = float(expense_credit)
        payment_convert = float(payment)
        discount_convert = float(discount)

    ws.update_cell(2, 7, expense_credit_convert)
    ws.update_cell(2, 8, payment_convert)
    ws.update_cell(2, 9, discount_convert)

    return (expense_credit_convert, payment_convert, discount_convert)


def write_values_in_sheet(ws: Worksheet, values: tuple):
    col = ws.find("Tag", in_row=1).col

    for item in values:
        col += 1
        ws.update_cell(2, col, item)
