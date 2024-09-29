# Yelp - Análise de Sentimento

Este projeto realiza a análise de sentimento sobre os dados do Yelp usando Prefect para orquestração, com processamento paralelo de blocos de dados e consolidação dos resultados.

## Estrutura do Projeto

- **data/raw/**: Contém os arquivos JSON brutos.
- **data/staging/**: Contém os arquivos Parquet após a conversão e pré-processamento.
- **data/processed/**: Contém os resultados processados e consolidados.
- **flows/**: Contém os fluxos Prefect para conversão e processamento de dados.
- **my_project/**: Contém as funções principais de conversão, processamento e análise de sentimento.

## Como Executar:

### 1. Converter os dados brutos para Parquet
```bash
python flows/convert_data_flow.py
```

### 2. Executar a análise de sentimento e consolidar os resultados

```bash
python flows/sentiment_analysis_flow.py
```

### Dependências:
Instale as dependências do projeto:

```bash
pip install pandas pyarrow vaderSentiment prefect
```

### Observações:
- Certifique-se de que os arquivos business.json e review.json estejam no diretório data/raw/.

- Escolha o formato de saída consolidado (Parquet ou CSV) alterando o parâmetro output_format.

### Conclusão:

### Conclusão

Esta versão do projeto está documentada e organizada para garantir a fácil compreensão por outros desenvolvedores. Com Prefect para orquestração, o fluxo do projeto é automatizado e os dados são processados de forma eficiente.