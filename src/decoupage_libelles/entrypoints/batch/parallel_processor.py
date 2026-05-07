"""
Traitement parallèle d'un fichier par chunks via l'API FastAPI.
"""
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import Callable, Iterator, List

from decoupage_libelles.entrypoints.batch.data_preparation import build_voie_column, filter_majic


def process_chunk(chunk: pd.DataFrame, voie_columns: List[str], api_call: Callable) -> pd.DataFrame:
    """
    Traite un chunk :
    1. Construit la colonne de libellé de voie
    2. Appelle l'API de découpage
    3. Joint les résultats au chunk d'origine
    """
    chunk, voie_col = build_voie_column(chunk, voie_columns)

    if chunk[voie_col].notna().sum() == 0:
        return chunk

    libelles = chunk[voie_col].dropna().tolist()
    response_data = api_call(libelles)

    if response_data is None:
        return chunk

    rows = [{"origin": key, **value} for item in response_data for key, value in item.items()]
    df_response = (
        pd.DataFrame(rows)
        .rename(columns={
            "origin":            voie_col,
            "typeVoie":          "type_voie_parse",
            "libelleVoie":       "libelle_voie_parse",
            "complementAdresse": "complement_adresse",
            "complementAdresse2":"complement_adresse2",
        })
        .drop(columns=["numero", "indice_rep"], errors="ignore")
    )

    return chunk.merge(df_response, on=voie_col, how="left")


def run_parallel(
    chunks: Iterator[pd.DataFrame],
    total_chunks: int,
    voie_columns: List[str],
    api_call: Callable,
    num_threads: int,
) -> pd.DataFrame:
    """
    Lance le traitement de tous les chunks en parallèle et retourne le DataFrame final.
    """
    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(process_chunk, chunk, voie_columns, api_call): i
            for i, chunk in enumerate(chunks)
        }
        for future in tqdm(as_completed(futures), total=total_chunks, desc="Traitement des chunks"):
            results.append(future.result())

    final_df = pd.concat(results, ignore_index=True)
    return filter_majic(final_df)
