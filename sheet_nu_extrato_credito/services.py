def update_all_pages():
    from gspread import WorksheetNotFound
    from . import spreads
    from time import sleep

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
