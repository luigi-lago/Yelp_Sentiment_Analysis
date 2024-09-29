"""
Módulo responsável pela conversão dos arquivos JSON brutos para Parquet e
aplicação de pré-processamento básico nos dados.
"""
import pandas as pd

def convert_business_json_to_parquet():
    """
    Converte o arquivo business.json para Parquet, renomeando e removendo
    registros inválidos ou com dados faltantes.
    """
    try:
        # Carregar o arquivo JSON original
        business_df = pd.read_json('data/raw/business.json', lines=True)

        # Renomear a coluna 'stars' para 'avg_stars' para indicar a média de avaliações do negócio
        business_df = business_df.rename(columns={'stars': 'avg_stars'})

        # Remover registros com valores faltantes nos campos críticos
        business_df = business_df.dropna(subset=['business_id', 'avg_stars'])

        # Salvar o DataFrame em formato Parquet na camada staging
        business_df.to_parquet('data/staging/business.parquet', index=False, engine='pyarrow')
        print("business.json convertido para Parquet com sucesso.")
    
    except Exception as e:
        print(f"Erro ao processar business.json: {e}")


def convert_review_json_to_parquet_in_chunks(chunksize=100_000):
    """
    Converte o arquivo review.json para Parquet em blocos, aplicando limpeza
    básica e normalização do texto das avaliações.
    
    chunksize: Número de linhas a serem processadas por bloco.
    """
    try:
        for i, chunk in enumerate(pd.read_json('data/raw/review.json', lines=True, chunksize=chunksize)):
            # Renomear 'stars' para 'user_stars', representando a avaliação dada pelo usuário
            chunk = chunk.rename(columns={'stars': 'user_stars'})

            # Remover registros com campos críticos vazios
            chunk = chunk.dropna(subset=['business_id', 'review_id', 'text', 'user_stars'])

            # Normalizar o texto removendo espaços extras e convertendo para minúsculas
            chunk['text'] = chunk['text'].str.strip().str.lower()

            # Salvar cada bloco processado em Parquet
            chunk.to_parquet(f'data/staging/review_part_{i}.parquet', index=False, engine='pyarrow')
            print(f"Bloco {i} do review.json convertido para Parquet com sucesso.")
    
    except Exception as e:
        print(f"Erro ao processar review.json em blocos: {e}")
