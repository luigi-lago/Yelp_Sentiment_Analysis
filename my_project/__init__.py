"""
Arquivo __init__.py para o pacote my_project.
Este arquivo facilita as importações dos módulos de data_processing e sentiment_analysis.
"""

# Importar funções do módulo data_processing:
from .data_processing import (
    convert_business_json_to_parquet,
    convert_review_json_to_parquet_in_chunks
)

# Importar funções do módulo sentiment_analysis:
from .sentiment_analysis import (
    process_data_in_chunks,
    consolidate_results
)