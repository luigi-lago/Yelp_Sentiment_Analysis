"""
Flow Prefect para orquestrar o processamento de dados, análise de sentimento
e consolidação dos resultados em um único arquivo.
"""

import sys
import os

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prefect import flow, task
from my_project import process_data_in_chunks, consolidate_results

@task
def run_sentiment_analysis():
    """
    Task para processar os dados e aplicar a análise de sentimento.
    """
    process_data_in_chunks()

@task
def run_consolidate_results():
    """
    Task para consolidar os resultados processados em um único arquivo.
    """
    consolidate_results()

@flow
def sentiment_analysis_flow():
    """
    Flow principal que coordena a execução da análise de sentimento e consolidação dos dados.
    """
    run_sentiment_analysis()
    run_consolidate_results()

if __name__ == "__main__":
    sentiment_analysis_flow.with_options(name="Flow_Analise_Sentimento")()