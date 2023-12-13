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

        spreads.calculate_expense_credit(month)
        spreads.calculate_payment(month)


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
    while True:
        print("Deseja fazer operação em qual opção: \n1 - CREDITO\n2 - CONTA\n")
        opc = int(input("Insira o valor: "))

        if opc == 1:
            sheet_nu_extrato_credito()
            break

        elif opc == 2:
            sheet_nu_extrato_conta()
            break

        else:
            print(
                "Opção inválida digite o número correto de sua opção: \n1 - CREDITO\n2- - CONTA"
            )


if __name__ == "__main__":
    main()
