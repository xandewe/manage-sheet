def sheet_teste_integracao():
    from sheet_teste_integracao.services import insert_titles
    from sheet_teste_integracao.spreads import set_title

    titles = insert_titles()
    set_title(*titles)


def main():
    sheet_teste_integracao()


if __name__ == "__main__":
    main()
