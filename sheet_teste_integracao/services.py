def insert_titles():
    titles = []
    while True:
        title = input(f"Digite o cabeçalho desejado: ").title()
        titles.append(title)
        exit = input(f"Encerrar s/n: ").lower()

        if exit == "s":
            break

    return titles
