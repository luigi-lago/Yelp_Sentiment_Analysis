"""
Flow Prefect para orquestrar a conversão dos dados JSON brutos para Parquet
e aplicação de pré-processamento.
"""

import sys
import os

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prefect import flow, task
from my_project import convert_business_json_to_parquet, convert_review_json_to_parquet_in_chunks

@task
def run_convert_business_json():
    """
    Task para executar a conversão do arquivo business.json para Parquet.
    """
    convert_business_json_to_parquet()

@task
def run_convert_review_json():
    """
    Task para executar a conversão do arquivo review.json para Parquet em blocos.
    """
    convert_review_json_to_parquet_in_chunks()

@flow
def convert_data_flow():
    """
    Flow principal que coordena a execução das tasks de conversão de dados.
    """
    run_convert_business_json()
    run_convert_review_json()

if __name__ == "__main__":
    convert_data_flow()
