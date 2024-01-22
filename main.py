def sheet_nu_extrato_credito():
    from sheet_nu_extrato_credito import spreads, services
    import os

    option = "\n1 - PROCESSAMENTO AUTOMATICO DE TODOS OS MESES\n2 - PROCESSAMENTO POR MES\n3 - POPULAR DB\n0 - SAIR\n"

    while True:
        print(f"\nDeseja qual operação (CREDITO): {option}")
        opc = int(input("Insira o valor: "))

        if opc == 0:
            break

        elif opc == 1:
            services.update_all_pages()

        elif opc == 2:
            month = int(
                input(
                    "Digite o numero do mês que deseja processar os dados (CREDITO): "
                )
            )

            spreads.calculate_expense_credit(12 + month)
            spreads.calculate_payment(12 + month)

        elif opc == 3:
            path = "./package_csv"

            print("Verifique se o arquivo CSV está presente em package.csv")
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
                print("Arquivo não encontrado no diretório")

        else:
            print(f"Opção inválida digite o número correto de sua opção: {option}")


def sheet_nu_extrato_conta():
    from sheet_nu_extrato_conta import spreads, services
    import os

    option = "\n1 - PROCESSAMENTO AUTOMATICO DE TODOS OS MESES\n2 - PROCESSAMENTO POR MES\n3 - POPULAR DB\n0 - SAIR\n"

    while True:
        print(f"\nDeseja qual operação (CONTA): {option}")
        opc = int(input("Insira o valor: "))

        if opc == 0:
            break

        elif opc == 1:
            services.update_all_pages()

        elif opc == 2:
            month = int(
                input("Digite o numero do mês que deseja processar os dados (CONTA): ")
            )

            spreads.calculate_income(month)
            spreads.calculate_expense(month)

        elif opc == 3:
            path = "./package_csv"

            print("Verifique se o arquivo CSV está presente em package.csv")
            month = input("Insira o mês desejado (ex: 01): ").strip()
            year = input("Insira o ano desejado (ex: 2023): ").strip()
            month_list = [
                "JAN",
                "FEV",
                "MAR",
                "ABR",
                "MAI",
                "JUN",
                "JUL",
                "AGO",
                "SET",
                "OUT",
                "NOV",
                "DEZ",
            ]

            files = os.listdir(path)

            file_csv = ""

            for file in files:
                chosen_month = month_list[int(month) - 1]
                if year in file and chosen_month in file:
                    file_csv = file
                    print(f"\nARQUIVO ENCONTRADO {file}\n")
                    break

            if file_csv:
                services.populate_database_with_account(file_csv)

            else:
                print("Arquivo não encontrado no diretório")

        else:
            print(f"Opção inválida digite o número correto de sua opção: {option}")


def main():
    from utils import create_template
    import os

    sheet_id = input("Qual o ID do Sheet será manipulado: ").strip()
    os.environ["SHEET_NU_EXTRATO"] = sheet_id


    option = "\n1 - CREDITO\n2 - CONTA\n3 - TEMPLATE PAGES SHEET\n0 - SAIR\n"

    while True:
        print(f"Deseja fazer operação em qual opção: {option}")
        opc = int(input("Insira o valor: "))

        if opc == 0:
            break

        if opc == 1:
            sheet_nu_extrato_credito()

        elif opc == 2:
            sheet_nu_extrato_conta()

        elif opc == 3:
            key = input(f"Qual a key de sua planilha: ").strip()
            create_template(key)

        else:
            print(f"Opção inválida digite o número correto de sua opção: {option}")


if __name__ == "__main__":
    main()
