"""
Módulo responsável pelo processamento dos dados e aplicação da análise de sentimento
usando a biblioteca VaderSentiment, seguido da consolidação dos resultados processados.
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


def get_sentiment(text):
    """
    Função que aplica a análise de sentimento no texto usando VaderSentiment.
    
    param text: Texto da avaliação a ser analisado.
    return: Classificação do sentimento (positivo, negativo, neutro).
    """
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def process_chunk(chunk):
    """
    Função auxiliar para aplicar a análise de sentimento em um bloco de dados.
    
    param chunk: Bloco de dados contendo texto de avaliações.
    return: Bloco de dados com a coluna 'sentimento' adicionada.
    """
    chunk['sentimento'] = chunk['text'].apply(get_sentiment)
    return chunk


def process_data_in_chunks():
    """
    Processa os dados de reviews em blocos, aplica a análise de sentimento e salva
    os resultados processados na camada processed.
    """
    try:
        # Carregar os dados dos negócios (business.parquet)
        business_df = pd.read_parquet('data/staging/business.parquet')
        
        # Detectar o número de núcleos disponíveis para processamento paralelo
        num_workers = multiprocessing.cpu_count()
        i = 0

        while True:
            try:
                # Carregar o bloco de reviews
                review_chunk = pd.read_parquet(f'data/staging/review_part_{i}.parquet')

                # Fazer o join entre os reviews e os negócios
                dados_transformados = pd.merge(review_chunk, business_df, on='business_id', how='inner')

                # Dividir os dados em chunks para processamento paralelo
                chunk_size = len(dados_transformados) // num_workers
                chunks = [dados_transformados.iloc[j:j + chunk_size] for j in range(0, len(dados_transformados), chunk_size)]

                # Aplicar a análise de sentimento em paralelo
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    processed_chunks = list(executor.map(process_chunk, chunks))

                # Concatenar os resultados processados
                dados_transformados = pd.concat(processed_chunks)

                # Selecionar as colunas relevantes e salvar o bloco processado
                dados_transformados = dados_transformados[['business_id', 'name', 'city', 'state', 'avg_stars',
                                                           'review_count', 'review_id', 'user_id', 'user_stars',
                                                           'date', 'useful', 'funny', 'cool', 'text', 'sentimento']]
                
                dados_transformados.to_parquet(f'data/processed/review_sentiment_part_{i}.parquet', index=False, engine='pyarrow')
                print(f"Bloco {i} processado e salvo com sucesso.")
                i += 1

            except FileNotFoundError:
                print("Processamento de todos os blocos concluído.")
                break

    except Exception as e:
        print(f"Erro no processamento dos dados: {e}")


def consolidate_results(output_format='parquet'):
    """
    Consolida todos os arquivos processados em um único arquivo.
    
    param output_format: Formato de saída do arquivo consolidado ('parquet' ou 'csv').
    """
    try:
        # Diretório dos arquivos processados
        processed_dir = '../data/processed/'
        processed_files = list(processed_dir.glob('*.parquet'))

        if not processed_files:
            print("Nenhum arquivo processado encontrado na pasta 'processed'.")
            return

        # Concatenar todos os arquivos processados em um único DataFrame
        consolidated_df = pd.concat([pd.read_parquet(file) for file in processed_files])

        # Salvar o arquivo consolidado
        output_path = processed_dir / f'review_sentiment_consolidated.{output_format}'
        
        if output_format == 'parquet':
            consolidated_df.to_parquet(output_path, index=False, engine='pyarrow')
        elif output_format == 'csv':
            consolidated_df.to_csv(output_path, index=False)
        else:
            raise ValueError("Formato de saída não suportado. Escolha 'parquet' ou 'csv'.")

        print(f"Resultados consolidados salvos em {output_path}")
    
    except Exception as e:
        print(f"Erro ao consolidar os resultados: {e}")
