# Introdução

A aplicação em Python proposta visa simplificar o gerenciamento financeiro ao importar dados do Nubank em formato CSV para um sheet de controle. Com funcionalidades intuitivas, o programa oferece uma abordagem eficiente para analisar despesas e receitas, proporcionando aos usuários uma ferramenta ágil e personalizável para otimizar o controle financeiro de maneira prática e eficaz.

## Configurações GCP (Google Cloud Platafform)
- Crie um projeto no GCP e adicione a API do Google Sheets;
- Gerar suas credenciais pelo GCP e criar uma key do tipo JSON;
- Fazer o download e colocar o arquivo JSON na raiz da aplicação com o nome `credentials.json`;
- Copie o `client_email` do arquivo *credentials.json* e compartilhe o sheets com esse email como editor;
- Copie o ID da planilha que deseja manipular e cole em seu **.env** (DICA: para pegar o ID da planilha abra ela e copie tudo que está entre as "/" após `docs.google.com/spreadsheets/d/`)

## Configurações variáveis de ambiente
- **SHEET_NU_EXTRATO** = Esta variável é responsável por armazenar o ID da planilha que será manipulada. Certifique-se de fornecer o ID correto para garantir a integração adequada com a planilha desejada.
- **GOOGLE_APPLICATION_CREDENTIALS** = Esta variável armazena o caminho do arquivo de credenciais em formato JSON. Siga cuidadosamente os passos da documentação, e você não precisará ajustar diretamente esta variável.
- **URL** = A variável URL armazena o endereço da API utilizada para o armazenamento dos dados. Certifique-se de inserir a URL correta para garantir a comunicação eficaz entre o aplicativo e o serviço de armazenamento de dados. (em desenvolvimento).
- **SAVE_CSV_PATH** = Indica o caminho onde será salvo o novo CSV processado para utilização no sheets

## Tecnologias utilizadas
- Python
- Gspread
- Gspread-formatting
- GCP
- Google-auth
- Pandas

## Funcionalidades
- Criar páginas padronizadas no Google Sheets, destinadas a armazenar dados em formato CSV referentes aos diferentes meses associados às informações da conta e aos dados de crédito
- Processamento dos dados inseridos em uma página referente ao mês indicado pelo usuário, com o objetivo de identificar e categorizar transações financeiras como entradas ou saídas. Os valores associados a essas transações são calculados e classificados em diferentes categorias divididos entre o tipo conta e o tipo crédito:
  - **Tipo conta**: As categorias são `Entrada`, `Estorno/Reembolso`, `Resgate de Investimento`, `Saída`, `Pagamento de Fatura` e `Investimento`. Para aprimorar a experiência do usuário e a organização dos dados, dois espaços adicionais são disponibilizados: `Sub tag` e `Tag`. O campo `Sub tag` permite que o usuário atribua um nome mais intuitivo ou identificador personalizado a cada transação, facilitando a referência e compreensão das operações. Já o campo `Tag` oferece a possibilidade de adicionar rótulos ou etiquetas específicas a cada transação, proporcionando uma forma adicional de categorização e organização personalizada.
  - **Tipo crédito**: As categorias são `Total gasto` e `Pagamento`, além dos campos adicionais `Sub tag` e `Tag` referidos no item acima.
- Processamento automatizado de dados financeiros, eliminando a necessidade de inserção manual mês a mês. A automação abrange tanto o **tipo de conta** quanto o **tipo de crédito**, garantindo que todas as transações sejam processadas e categorizadas adequadamente. **DESCONTINUADO**
- Popular o banco de dados com o arquivo CSV do Nubank, para realizar a operação é necessário extrair os arquivos CSV do Nubank referentes ao cartão de crédito e à conta corrente. Esses arquivos devem ser depositados no diretório denominado package.csv. É crucial observar que o nome do arquivo CSV não deve ser modificado. Ao escolher esta opção, será solicitado que você informe o mês e o ano desejados para o qual o arquivo CSV correspondente esteja localizado no diretório mencionado. Posteriormente, o programa efetuará uma requisição automatizada para importar os dados contidos no arquivo CSV para o banco de dados, preenchendo assim as informações correspondentes ao período selecionado.
- Processar CSV e a partir dos dados obtidos, construir um novo csv com dados tratados e distribuição de tags e sub tags de forma inteligente para importar no sheets (Em construção).

## Possíveis erros mapeados
- Caso dê o erro de dado não encontrado a variável de ambiente **(SHEET_NU_EXTRATO)** pode estar incorreta.