from gspread import WorksheetNotFound
from . import spreads, ALIMENTACAO, CASA, TRANSPORTE
from time import sleep
import csv
import os
from decimal import Decimal
import requests
from . import url
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


def read_csv(file: str) -> pd.DataFrame:
    try:
        data_frame = pd.read_csv(file)
    except FileNotFoundError as _:
        raise FileNotFoundError(f"Arquivo {file} não encontrado")

    return data_frame


def processing_tag_and_subtags(dt: pd.DataFrame, rows: int):
    description_list = dt["Descrição"]
    sub_tags = ["" for _ in range(rows)]
    tags = ["" for _ in range(rows)]

    for index, description in enumerate(description_list):
        for item in ALIMENTACAO:
            if item in description.upper():
                tags[index] = "Alimentação"
                sub_tags[index] = item.title()

        for item in TRANSPORTE:
            if item in description.upper():
                tags[index] = "Transporte"
                sub_tags[index] = item.title()

        for item in CASA:
            if item in description.upper():
                tags[index] = "Casa"
                sub_tags[index] = item.title()

    dt.insert(4, "Sub Tag", sub_tags)
    dt.insert(5, "Tag", tags)


def processing_income(dt: pd.DataFrame, rows: int):
    value_list = dt["Valor"]
    income = ["" for _ in range(rows)]
    income[0] = 0

    for index, value in enumerate(value_list):
        convert_number = Decimal(str(value))
        description = dt.Descrição[index]

        if convert_number > 0 and (
            "estorno" not in description.lower()
            and "reembolso recebido" not in description.lower()
            and "resgate" not in description.lower()
        ):
            income[0] += convert_number

    dt.insert(6, "Entrada", income)


def processing_return_money(dt: pd.DataFrame, rows: int):
    value_list = dt["Valor"]
    return_money = ["" for _ in range(rows)]
    return_money[0] = 0

    for index, value in enumerate(value_list):
        convert_number = Decimal(str(value))
        description = dt.Descrição[index]

        if convert_number > 0 and (
            "estorno" in description.lower()
            or "reembolso recebido" in description.lower()
        ):
            return_money[0] += convert_number

    dt.insert(7, "Estorno/Reembolso", return_money)


def processing_rescue(dt: pd.DataFrame, rows: int):
    value_list = dt["Valor"]
    rescue = ["" for _ in range(rows)]
    rescue[0] = 0

    for index, value in enumerate(value_list):
        convert_number = Decimal(str(value))
        description = dt.Descrição[index]

        if convert_number > 0 and "resgate" in description.lower():
            rescue[0] += convert_number

    dt.insert(8, "Resgate Invest.", rescue)


def processing_csv_data(dt: pd.DataFrame) -> pd.DataFrame:
    rows = dt.count().Data

    processing_tag_and_subtags(dt, rows)
    processing_income(dt, rows)
    processing_return_money(dt, rows)
    processing_rescue(dt, rows)
