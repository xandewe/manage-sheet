from gspread import WorksheetNotFound
from . import spreads
from time import sleep
import csv
import os
from decimal import Decimal
import requests
from utils import url


def update_all_pages():
    month = 1

    for index in range(13, 25):
        try:
            print(f"CALCULANDO MÊS {month}")
            spreads.calculate_expense_credit(index)
            spreads.calculate_payment(index)
            print(f"MÊS {month} FINALIZADO!!!\n")
            month += 1

            # Necessário para evitar status code 429
            sleep(60)

        except WorksheetNotFound as _:
            print(f"WorkSheet do mês {index} não encontrada!")


def populate_database_with_credit(file_csv: str):
    file_csv = file_csv.split(".")[0]
    file_path = os.path.join("./package_csv", f"{file_csv}.csv")

    counter = 0
    counter_payment = 0

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for line in reader:
                if reader.line_num > 1:
                    if line[1] != "payment":
                        fields = ["created_at", "description", "name", "value"]

                        data = dict(zip(fields, line))

                        data["value"] = Decimal(data["value"])
                        data.update({"type": "Credit Card"})
                        data.update({"status": "Done"})

                        _, year, month = file_csv.split("-")
                        data.update({"year_month_reference": f"{year}-{month}"})

                        response = requests.post(url, data, verify=False)

                        counter += 1

                    else:
                        counter_payment += 1

                    print(f"Processando ...")

            print(
                f"\n{counter+counter_payment} dados processados para o DB com sucesso\n{counter_payment} dados de pagamento\n{counter} dados de saída"
            )

    else:
        print(f"Arquivo não encontrado no diretório | {file_path}")
