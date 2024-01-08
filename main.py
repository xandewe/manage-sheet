def sheet_nu_extrato_credito():
    from sheet_nu_extrato_credito import spreads, services

    update_automatic = input(
        "Deseja fazer atualização automatica de todos os meses (s/n): "
    ).lower()

    if update_automatic == "s":
        services.update_all_pages()

    else:
        month = int(
            input("Digite o numero do mês que deseja processar os dados (CREDITO): ")
        )

        spreads.calculate_expense_credit(12 + month)
        spreads.calculate_payment(12 + month)


def sheet_nu_extrato_conta():
    from sheet_nu_extrato_conta import spreads, services

    update_automatic = input(
        "Deseja fazer atualização automatica de todos os meses (s/n): "
    ).lower()

    if update_automatic == "s":
        services.update_all_pages()

    else:
        month = int(
            input("Digite o numero do mês que deseja processar os dados (CONTA): ")
        )

        spreads.calculate_income(month)
        spreads.calculate_expense(month)


def main():
    from utils import create_template
    from dotenv import load_dotenv
    import os

    load_dotenv()

    key = os.getenv("SHEET_NU_EXTRATO")

    while True:
        print(
            "Deseja fazer operação em qual opção: \n1 - CREDITO\n2 - CONTA\n3 - TEMPLATE WORKSHEETS\n"
        )
        opc = int(input("Insira o valor: "))

        if opc == 1:
            sheet_nu_extrato_credito()
            break

        elif opc == 2:
            sheet_nu_extrato_conta()
            break

        elif opc == 3:
            create_template(key)
            break

        else:
            print(
                "Opção inválida digite o número correto de sua opção: \n1 - CREDITO\n2- - CONTA"
            )


if __name__ == "__main__":
    main()
