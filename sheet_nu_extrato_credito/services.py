def update_all_pages():
    from gspread import WorksheetNotFound
    from . import spreads
    from time import sleep

    for index in range(1, 13):
        try:
            print(f"CALCULANDO MÊS {index}")
            spreads.calculate_expense_credit(index)
            spreads.calculate_payment(index)
            print(f"MÊS {index} FINALIZADO!!!\n")

            # Necessário para evitar status code 429
            sleep(60)

        except WorksheetNotFound as _:
            print(f"WorkSheet do mês {index} não encontrada!")
