def sheet_nu_extrato_credito(key):
    from sheet_nu_extrato_credito import spreads, services
    import os
    from utils import verify_sheet
    from exceptions import WorksheetException

    option = "\n1 - PROCESSAMENTO SHEET POR MES\n2 - POPULAR DB\n0 - SAIR\n"

    while True:
        print(f"\nDeseja qual operação (CREDITO): {option}")
        opc = int(input("Insira o valor: "))

        if opc == 0:
            break

        elif opc == 1:
            month = int(
                input(
                    "\nDigite o numero do mês que deseja processar os dados (CREDITO): "
                )
            )

            print("PROCESSANDO DADOS NO SHEET...")

            try:
                month += 12
                ws, values_list, quantity_columns = verify_sheet(month, key)
                spreads.write_sheet_headers(ws, quantity_columns)
                values_calc = spreads.cash_inflows_and_outflows_analysis(
                    ws, values_list
                )
                spreads.write_values_in_sheet(ws, values_calc)
            except WorksheetException as err:
                print(err)

        elif opc == 2:
            path = "./package_csv"

            print("\nVerifique se o arquivo CSV está presente em package.csv")
            month = input("Insira o mês desejado (ex: 01): ").strip()
            year = input("Insira o ano desejado (ex: 2023): ").strip()

            files = os.listdir(path)

            file_csv = ""

            for file in files:
                file_csv = f"nubank-{year}-{month}.csv"
                if file_csv in file:
                    file_csv = file
                    print(f"\nARQUIVO ENCONTRADO {file}\n")
                    break

            if file_csv:
                services.populate_database_with_credit(file_csv)

            else:
                print("\nArquivo não encontrado no diretório")

        else:
            print(f"\nOpção inválida digite o número correto de sua opção: {option}")


def sheet_nu_extrato_conta(key):
    from sheet_nu_extrato_conta import (
        spreads,
        services,
        MONTH_LIST,
        PACKAGE_PATH,
        standard_month,
        standard_year,
        csv_path,
    )
    import os
    from utils import verify_sheet
    from exceptions import WorksheetException

    option = "\n1 - PROCESSAMENTO SHEET POR MES\n2 - POPULAR DB\n3 - GERAR CSV PROCESSADO\n4 - FORMATAR SHEETS COM CORES\n0 - VOLTAR\n"

    while True:
        print(f"\nDeseja qual operação (CONTA): {option}")
        opc = int(input("Insira o valor: "))

        if opc == 0:
            break

        elif opc == 1:
            month = int(
                input(
                    "\nDigite o numero do mês que deseja processar os dados (CONTA): "
                )
            )

            print("PROCESSANDO DADOS NO SHEET...")

            try:
                ws, values_list, quantity_columns = verify_sheet(month, key)
                spreads.write_sheet_headers(ws, quantity_columns)
                values_calc = spreads.cash_inflows_and_outflows_analysis(
                    ws, values_list
                )
                spreads.write_values_in_sheet(ws, values_calc)
            except WorksheetException as err:
                print(err)

        elif opc == 2:
            print("\nVerifique se o arquivo CSV está presente em package.csv")
            month = (
                input(
                    f"Insira o mês desejado (ex: 01) pressione enter para {standard_month}: "
                ).strip()
                or standard_month
            )
            year = (
                input(
                    f"Insira o ano desejado (ex: 2023) pressione enter para {standard_year}: "
                ).strip()
                or standard_year
            )

            files = os.listdir(PACKAGE_PATH)

            file_csv = ""

            for file in files:
                chosen_month = MONTH_LIST[int(month) - 1]
                if year in file and chosen_month in file:
                    file_csv = file
                    print(f"\nARQUIVO ENCONTRADO {file}\n")
                    break

            if file_csv:
                services.populate_database_with_account(file_csv)

            else:
                print("\nArquivo não encontrado no diretório")

        if opc == 3:
            print("\nVerifique se o arquivo CSV está presente em package.csv")
            month = (
                input(
                    f"Insira o mês desejado (ex: 01) pressione enter para {standard_month}: "
                ).strip()
                or standard_month
            )
            year = (
                input(
                    f"Insira o ano desejado (ex: 2023) pressione enter para {standard_year}: "
                ).strip()
                or standard_year
            )

            files = os.listdir(PACKAGE_PATH)

            file_csv = ""

            for file in files:
                chosen_month = MONTH_LIST[int(month) - 1]
                if year in file and chosen_month in file:
                    file_csv = file
                    print(f"\nARQUIVO ENCONTRADO {file}\n")
                    break

            if file_csv:
                path = f"{PACKAGE_PATH}/{file_csv}"
                dt = services.read_csv(path)
                dt_formatted = services.processing_csv_data(dt)
                services.generate_csv(dt_formatted, file_csv)
                print(f"\nARQUIVO GERADO EM {csv_path}\n")

            else:
                print("\nArquivo não encontrado no diretório")

        if opc == 4:
            month = int(
                input(
                    "\nDigite o numero do mês que deseja processar os dados (CONTA): "
                )
            )

            print("PROCESSANDO DADOS NO SHEET...")

            try:
                ws, values_list, quantity_columns = verify_sheet(month, key)
                values_calc = spreads.cash_inflows_and_outflows_analysis(
                    ws, values_list
                )
            except WorksheetException as err:
                print(err)

        else:
            print(f"\nOpção inválida digite o número correto de sua opção: {option}")


def main():
    from utils import create_template
    import os

    standard_key = os.getenv("SHEET_NU_EXTRATO")

    print(f"Key de sheet padrão: {standard_key}")

    key = (
        input(
            "Qual o ID do Sheet será manipulado, (pressione enter para sheet padrão): "
        ).strip()
        or standard_key
    )
    os.environ["SHEET_NU_EXTRATO"] = key

    option = "\n1 - CREDITO\n2 - CONTA\n3 - TEMPLATE PAGES SHEET\n0 - SAIR\n"

    while True:
        print(f"\nDeseja fazer operação em qual opção: {option}")
        opc = int(input("Insira o valor: "))

        if opc == 0:
            break

        if opc == 1:
            sheet_nu_extrato_credito(key)

        elif opc == 2:
            sheet_nu_extrato_conta(key)

        elif opc == 3:
            create_template(key)

        else:
            print(f"\nOpção inválida digite o número correto de sua opção: {option}")


if __name__ == "__main__":
    main()
