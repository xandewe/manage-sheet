from utils import worksheet
from . import key
import csv

ws = worksheet(key, 1)


def convert_values_sheet():
    values_list = ws.col_values(2)
    line = 2

    for item in values_list[1:]:
        convert_number = float(item)
        ws.update_cell(line, 2, convert_number)


def calculate_expense():
    ws.update_cell(1, 7, "Saida")
    ws.update_cell(1, 8, "Pagamento fatura credito")
    ws.update_cell(1, 9, "Investido")

    # values_list = ws.col_values(2)
    values_list = ws.get_values()

    expense = 0
    invoice_card = 0
    invested = 0

    for item in values_list[1:]:
        # import ipdb

        # ipdb.set_trace()

        date, value, id, description, *_ = item
        convert_number = float(value)

        if "aplicação rdb" in description.lower():
            invested += convert_number

        elif "pagamento de fatura" in description.lower():
            invoice_card += convert_number

        elif convert_number < 0:
            expense += convert_number

    ws.update_cell(2, 7, expense)
    ws.update_cell(2, 8, invoice_card)
    ws.update_cell(2, 9, invested)


def calculate_revenue():
    ws.update_cell(1, 5, "Entrada")
    ws.update_cell(1, 6, "Estorno/Reembolso")

    # values_list = ws.col_values(2)
    values_list = ws.get_values()

    revenue = 0
    reversal = 0

    for item in values_list[1:]:
        date, value, id, description, *_ = item
        convert_number = float(value)
        # import ipdb

        # ipdb.set_trace()
        if "estorno" in description.lower():
            reversal += convert_number

        elif convert_number > 0:
            revenue += convert_number

    ws.update_cell(2, 5, revenue)
    ws.update_cell(2, 6, reversal)
