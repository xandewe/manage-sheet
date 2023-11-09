import string
from utils import worksheet
from . import key

ws = worksheet(key)

def set_title(*args):
    counter = 0
    letter = string.ascii_uppercase

    for title in args:
        column = f"{letter[counter]}1"
        # Atualiza celula
        ws.update_acell(column, title)

        counter += 1


# Dicionario com os estados e as capitais
# capitais = {
#     "Paraíba": "João Pessoa",
#     "Santa Catarina": "Florianópolis",
#     "São Paulo": "São Paulo",
# }

# # Contador de colunas e celulas
# colums = 1
# cel = 2

# for estado, capital in capitais.items():
#     # Atualiza a celula 2 da coluna 1 com o nome do estado
#     worksheet.update_cell(cel, colums, estado)
#     # A coluna agora é a B
#     colums = 2
#     # Atualiza a celula 2 da coluna 2 com o nome da capital
#     worksheet.update_cell(cel, colums, capital)
#     # A coluna agora é a A
#     colums = 1
#     # Acrescenta mais um valor no numero da celula
#     cel += 1
