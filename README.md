# Yelp - Análise de Sentimento

Este projeto realiza uma análise de sentimentos nos dados de avaliações do Yelp. O objetivo é aplicar técnicas de Processamento de Linguagem Natural (NLP) para identificar o sentimento predominante (positivo, negativo ou neutro) nas avaliações dos clientes sobre os restaurantes. A solução usa processamento paralelo em blocos para lidar com grandes volumes de dados de forma eficiente e Prefect para orquestração dos fluxos de trabalho.

## Estrutura do Projeto:

O projeto está organizado em três camadas principais que simulam um pipeline de dados típico em Big Data:

- **data/raw/**: Contém os arquivos JSON brutos.

- **data/staging/**: Contém os arquivos Parquet após a conversão e pré-processamento.

- **data/processed/**: Contém os resultados processados e consolidados.

- **flows/**: Contém os fluxos Prefect para conversão e processamento de dados.

- **my_project/**: Contém as funções principais de conversão, processamento e análise de sentimento.

## Funcionalidades Principais:

- **Conversão de JSON para Parquet**: A conversão dos arquivos brutos do Yelp (JSON) para o formato Parquet otimiza o uso de memória e acelera as operações de leitura e escrita nos dados.

- **Processamento em Blocos**: O processamento das avaliações do Yelp é realizado em blocos (chunks) para evitar o esgotamento da memória ao lidar com grandes volumes de dados.

- **Análise de Sentimento**: Utilizando a biblioteca VADER, o projeto classifica as avaliações dos clientes em três categorias de sentimento: positivo, negativo e neutro.

- **Orquestração com Prefect**: Prefect automatiza o fluxo de dados, garantindo que cada etapa do pipeline seja executada corretamente e na ordem adequada. Isso inclui a conversão de dados, análise de sentimento e a consolidação dos resultados finais.

## Pré-requisitos:
Certifique-se de que os arquivos **business.json** e **review.json** estão disponíveis na pasta ``data/raw/``. Esses arquivos podem ser baixados a partir do <https://www.yelp.com/dataset>.

Instale as dependências do projeto:

```bash
pip install pandas pyarrow vaderSentiment prefect
```

## Como Executar:

### 1. Converter os dados brutos para Parquet:

Essa etapa converte os arquivos JSON brutos em Parquet, preparando os dados para o processamento posterior:

```bash
python flows/convert_data_flow.py
```

### 2. Executar a análise de sentimento e consolidar os resultados:

Esse comando executa a análise de sentimento em blocos de dados, utilizando processamento paralelo, e consolida os resultados processados na pasta ``data/processed/``:

```bash
python flows/sentiment_analysis_flow.py
```

### 3. Monitorar o Pipeline com Prefect Server:

Se quiser monitorar o fluxo de trabalho em tempo real usando a interface do Prefect, inicie o servidor localmente:

```bash
prefect server start
```
## Customização:

### Formato de saída:
O formato de saída dos dados consolidados pode ser ajustado para **Parquet** ou **CSV**. Para isso, modifique o parâmetro ``output_format`` no código de consolidação dos resultados, dentro da função ``consolidate_results()``.

## Observações:

- **Performance:** Certifique-se de que seu ambiente possui recursos suficientes para o processamento de grandes volumes de dados. O processamento em blocos ajuda a mitigar o uso excessivo de memória, mas grandes datasets ainda podem requerer algum tempo de processamento.

- **Paralelismo:** O projeto utiliza processamento paralelo para a aplicação da análise de sentimentos. Certifique-se de que sua máquina tem núcleos de CPU suficientes para tirar proveito desse paralelismo.


### Conclusão

Este projeto foi desenvolvido com o objetivo de simular uma arquitetura de Big Data em um ambiente local, otimizando o processamento e a análise de grandes volumes de dados com um pipeline automatizado e eficiente. Utilizando Prefect para orquestração e paralelismo com processamento em blocos, a solução é escalável e pode ser adaptada para diferentes volumes de dados. O código está bem estruturado para facilitar a manutenção e o entendimento por outros desenvolvedores.