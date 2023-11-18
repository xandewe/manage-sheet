def sheet_teste_integracao():
    from sheet_teste_integracao.services import insert_titles
    from sheet_teste_integracao.spreads import set_title

    titles = insert_titles()
    set_title(*titles)


def sheet_nu_ago():
    from sheet_nu_ago import spreads, services

    services.update_all_pages()

    # spreads.calculate_revenue()
    # spreads.calculate_expense()


def main():
    # sheet_teste_integracao()
    sheet_nu_ago()


if __name__ == "__main__":
    main()
