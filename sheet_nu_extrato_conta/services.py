from gspread import WorksheetNotFound
from . import spreads
from time import sleep
import csv
import os
from decimal import Decimal
import requests
from . import url


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

                    data.update({"status": "Done"})

                    response = requests.post(url, data)

                    counter += 1

                    print(f"Processando ...")

            print(f"\n{counter} dados processados para o DB com sucesso")

    else:
        print(f"Arquivo não encontrado no diretório | {file_path}")
