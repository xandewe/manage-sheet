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


def processing_tag_and_subtags(dt: pd.DataFrame):
    description_list = dt["Descrição"]
    sub_tags = ["" for _ in range(19)]
    tags = ["" for _ in range(19)]

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


def processing_csv_data(dt: pd.DataFrame) -> pd.DataFrame:
    processing_tag_and_subtags(dt)
