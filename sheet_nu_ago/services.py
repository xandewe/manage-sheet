
def update_all_pages():
    from gspread import WorksheetNotFound
    from . import spreads
    from time import sleep

    for index in range(1, 13):
        try:
            print(f"CALCULANDO MÊS {index}")
            spreads.calculate_revenue(index)
            spreads.calculate_expense(index)
            print(f"MÊS {index} FINALIZADO!!!")

            # Necessário para evitar status code 429
            if index == 5:
                sleep(15)

        except WorksheetNotFound as err:
            print(f"WorkSheet do mês {index} não encontrada!")
