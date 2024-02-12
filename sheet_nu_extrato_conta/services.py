from gspread import WorksheetNotFound
from utils import ALIMENTACAO, CASA, TRANSPORTE, csv_path, url
from time import sleep
import csv
import os
from decimal import Decimal, localcontext
import requests
from . import SHEET_COLUMNS_NAME, spreads
import pandas as pd


def update_all_pages():
    for index in range(1, 13):
        try:
            print(f"CALCULANDO MÊS {index}")
            spreads.calculate_income(index)
            spreads.calculate_expense(index)
            print(f"MÊS {index} FINALIZADO!!!\n")

            # Necessário para evitar status code 429
            sleep(60)

        except WorksheetNotFound as _:
            print(f"WorkSheet do mês {index} não encontrada!")


def populate_database_with_account(file_csv: str):
    file_csv = file_csv.split(".")[0]
    file_path = os.path.join("./package_csv", f"{file_csv}.csv")

    counter = 0

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for line in reader:
                if reader.line_num > 1:
                    fields = ["created_at", "value", "name"]
                    line.pop(2)
                    data = dict(zip(fields, line))
                    data["value"] = Decimal(data["value"])
                    data["created_at"] = "-".join(data["created_at"].split("/")[::-1])

                    if data["value"] < 0:
                        data.update({"type": "Expense"})
                        data["value"] = -1 * data["value"]

                    else:
                        data.update({"type": "Income"})

                    year_month_reference = data["created_at"][:-3]

                    data.update(
                        {"status": "Done", "year_month_reference": year_month_reference}
                    )

                    response = requests.post(url, data)

                    counter += 1

                    print(f"Processando ...")

            print(f"\n{counter} dados processados para o DB com sucesso")

    else:
        print(f"Arquivo não encontrado no diretório | {file_path}")


def processing_tag_and_subtags(dt: pd.DataFrame, rows: int) -> None:
    description_list = dt["Descrição"]
    sub_tags = ["" for _ in range(rows)]
    tags = ["" for _ in range(rows)]

    for index, description in enumerate(description_list):
        for item in ALIMENTACAO:
            if item in description.upper():
                tags[index] = "Alimentação"
                if item == "IFOOD":
                    sub_tags[index] = item.title()
                else:
                    sub_tags[index] = "Mercado"

        for item in TRANSPORTE:
            if item in description.upper():
                tags[index] = "Transporte"
                sub_tags[index] = item.title()

        for item in CASA:
            if item in description.upper():
                tags[index] = "Casa"
                sub_tags[index] = item.title()

    return (sub_tags, tags)


def analysis_cash_inflows_and_outflows_dataframe(dt: pd.DataFrame, rows: int):
    value_list = dt["Valor"]

    income = ["" for _ in range(rows)]
    income[0] = 0
    return_money = ["" for _ in range(rows)]
    return_money[0] = 0
    rescue = ["" for _ in range(rows)]
    rescue[0] = 0
    expense = ["" for _ in range(rows)]
    expense[0] = 0
    invoice_card = ["" for _ in range(rows)]
    invoice_card[0] = 0
    invested = ["" for _ in range(rows)]
    invested[0] = 0

    for index, value in enumerate(value_list):
        convert_number = Decimal(str(value))
        description = dt.Descrição[index]

        if convert_number > 0 and (
            "estorno" not in description.lower()
            and "reembolso recebido" not in description.lower()
            and "resgate" not in description.lower()
        ):
            income[0] += convert_number

        if convert_number > 0 and (
            "estorno" in description.lower()
            or "reembolso recebido" in description.lower()
        ):
            return_money[0] += convert_number

        if convert_number > 0 and "resgate" in description.lower():
            rescue[0] += convert_number

        if convert_number < 0 and (
            "aplicação rdb" not in description.lower()
            and "pagamento de fatura" not in description.lower()
        ):
            expense[0] += convert_number

        if convert_number < 0 and "pagamento de fatura" in description.lower():
            invoice_card[0] += convert_number

        if convert_number < 0 and "aplicação rdb" in description.lower():
            invested[0] += convert_number

    with localcontext() as ctx:
        ctx.prec = 10
        income[0] = str(income[0]).replace(".", ",")
        return_money[0] = str(return_money[0]).replace(".", ",")
        rescue[0] = str(rescue[0]).replace(".", ",")
        expense[0] = str(expense[0]).replace(".", ",")
        invoice_card[0] = str(invoice_card[0]).replace(".", ",")
        invested[0] = str(invested[0]).replace(".", ",")

    return (
        income,
        return_money,
        rescue,
        expense,
        invoice_card,
        invested,
    )


def processing_csv_data(dt: pd.DataFrame) -> pd.DataFrame:
    rows = dt.count().Data
    column = len(dt.columns)

    sub_tags, tags = processing_tag_and_subtags(dt, rows)

    dt.insert(column, SHEET_COLUMNS_NAME[0], sub_tags)
    column += 1
    dt.insert(column, SHEET_COLUMNS_NAME[1], tags)
    column += 1

    values_list = analysis_cash_inflows_and_outflows_dataframe(dt, rows)

    for index, header in enumerate(SHEET_COLUMNS_NAME[2:]):
        dt.insert(column, header, values_list[index])
        column += 1

    return dt


def generate_csv(dt: pd.DataFrame, file_name: str):
    format_name = file_name.split("_")
    format_name[1] = "PROCCESSED"
    file_name = "_".join(format_name)

    path = f"{csv_path}{file_name}"

    dt.to_csv(path, index=False)
