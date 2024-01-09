# Introdução

A aplicação em Python proposta visa simplificar o gerenciamento financeiro ao importar dados do Nubank em formato CSV para um sheet de controle. Com funcionalidades intuitivas, o programa oferece uma abordagem eficiente para analisar despesas e receitas, proporcionando aos usuários uma ferramenta ágil e personalizável para otimizar o controle financeiro de maneira prática e eficaz.

## Configurações GCP (Google Cloud Platafform)
- Crie um projeto no GCP e adicione a API do Google Sheets;
- Gerar suas credenciais pelo GCP e criar uma key do tipo JSON;
- Fazer o download e colocar o arquivo JSON na raiz da aplicação com o nome `credentials.json`;
- Copie o `client_email` do arquivo *credentials.json* e compartilhe o sheets com esse email como editor;
- Copie o ID da planilha que deseja manipular e cole em seu **.env** (DICA: para pegar o ID da planilha abra ela e copie tudo que está entre as "/" após `docs.google.com/spreadsheets/d/`)

## Tecnologias utilizadas
- Python
- Gspread
- Gspread-formatting
- GCP
- Google-auth

## Possíveis erros mapeados
- Caso dê o erro de dado não encontrado a variável de ambiente **(SHEET_NU_EXTRATO)** pode estar incorreta.