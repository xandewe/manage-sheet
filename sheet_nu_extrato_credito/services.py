from gspread import WorksheetNotFound
from . import spreads, SHEET_COLUMNS_NAME
from time import sleep
import csv
import os
from decimal import Decimal, localcontext
import requests
from utils import url, csv_path, processing_tag_and_subtags
import pandas as pd


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


def analysis_cash_inflows_and_outflows_dataframe(dt: pd.DataFrame, rows: int):
    value_list = dt["amount"]

    expense_credit = ["" for _ in range(rows)]
    expense_credit[0] = 0
    payment = ["" for _ in range(rows)]
    payment[0] = 0
    discount = ["" for _ in range(rows)]
    discount[0] = 0

    for index, value in enumerate(value_list):
        convert_number = Decimal(str(value))
        category = dt.category[index]

        if convert_number > 0:
            expense_credit[0] += convert_number

        elif "discount" in category and convert_number < 0:
            discount[0] += convert_number

        elif convert_number < 0:
            payment[0] += convert_number

    with localcontext() as ctx:
        ctx.prec = 10
        expense_credit[0] = str(expense_credit[0]).replace(".", ",")
        payment[0] = str(payment[0]).replace(".", ",")
        discount[0] = str(discount[0]).replace(".", ",")

    return (expense_credit, payment, discount)


def processing_csv_data(dt: pd.DataFrame) -> pd.DataFrame:
    rows = dt.count().date
    column = len(dt.columns)
    description_list = dt["title"]

    sub_tags, tags = processing_tag_and_subtags(description_list, rows)

    dt.insert(column, SHEET_COLUMNS_NAME[0], sub_tags)
    column += 1
    dt.insert(column, SHEET_COLUMNS_NAME[1], tags)

    values_list = analysis_cash_inflows_and_outflows_dataframe(dt, rows)

    for index, header in enumerate(SHEET_COLUMNS_NAME[2:]):
        column += 1
        dt.insert(column, header, values_list[index])

    return dt


def generate_csv(dt: pd.DataFrame, file_name: str):
    format_name = file_name.split("-")
    format_name.insert(1,"PROCCESSED")
    file_name = "-".join(format_name)
    import ipdb; ipdb.set_trace()

    path = f"{csv_path}{file_name}"

    dt.to_csv(path, index=False)
