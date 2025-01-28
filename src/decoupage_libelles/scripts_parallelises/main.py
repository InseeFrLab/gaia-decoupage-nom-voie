import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import s3fs
import warnings
import yaml
from yaml.loader import SafeLoader
import pyarrow.parquet as pq
from fastapi.testclient import TestClient
from decoupage_libelles.entrypoints.web.main_api import app, initialize_api


warnings.filterwarnings("ignore", category=FutureWarning)


def initialize_client():
    """Initialise le client FastAPI."""
    global client
    client = TestClient(app)


def process_chunk(chunk):
    """Traite un chunk de données avec l'API FastAPI."""
    chunk["nomVoieComplet"] = (
        chunk["type_voie"].fillna('') + ' ' + chunk["nom_voie"].fillna('')
    )
    if chunk[var_name_nom_voie].notna().sum() == 0:
        return chunk

    data = chunk[var_name_nom_voie].dropna().tolist()
    list_labels_voies = {"list_labels_voies": data}

    response = client.post("/analyse-libelles-voies", json=list_labels_voies)
    if response.status_code != 200:
        print(f"Erreur API : {response.status_code}")
        return chunk

    dict_reponse = response.json()["reponse"]
    rows = [
        {"origin": key, **value} for item in dict_reponse for key, value in item.items()
    ]
    df_response = pd.DataFrame(rows)

    # Joindre les résultats au chunk d'origine
    df_response.rename(columns={"origin": var_name_nom_voie}, inplace=True)
    merged_df = chunk.merge(df_response, on=var_name_nom_voie, how="left")
    return merged_df


def save_to_s3(df, file_type, output_file):
    """Sauvegarde le DataFrame final sur S3."""
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"]
    )

    with fs.open(output_file, "wb") as f:
        if file_type == "csv":
            df.to_csv(f, index=False)
        elif file_type == "parquet":
            df.to_parquet(f, engine="pyarrow", index=False)


def process_file(input_file, chunk_size, file_type, num_threads):
    """Lit un fichier en chunks et les traite en parallèle."""
    results = []
    with fs.open(input_file, "rb") as f:
        if file_type == "csv":
            reader = pd.read_csv(f, chunksize=chunk_size, dtype=str)
        elif file_type == "parquet":
            parquet_file = pq.ParquetFile(f)
            reader = parquet_file.iter_batches(batch_size=chunk_size)

        # Traitement parallèle des chunks
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {
                executor.submit(process_chunk, chunk.to_pandas() if file_type == "parquet" else chunk): chunk_id
                for chunk_id, chunk in enumerate(reader)
            }

            for future in tqdm(as_completed(futures), total=len(futures), desc="Traitement des chunks"):
                results.append(future.result())

    # Fusionner et sauvegarder les résultats finaux
    final_df = pd.concat(results, ignore_index=True)
    save_to_s3(final_df, file_type, output_file)


if __name__ == "__main__":
    # Chargement de la configuration
    with open("decoupage_libelles/scripts_parallelises/config.yml") as f:
        config = yaml.load(f, Loader=SafeLoader)

    # Variables globales
    global fs, var_name_nom_voie, output_file
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"]
    )

    input_file = f"s3://{config['s3_bucket']}/{config['input_path']}"
    output_file = input_file.replace(".csv", "_parsed.csv").replace(".parquet", "_parsed.parquet")
    var_name_nom_voie = config["var_name_nom_voie"]
    chunk_size = 10_000
    file_type = input_file.split(".")[-1]
    num_threads = 20  # Ajuster selon vos besoins

    # Initialisation
    initialize_api()
    initialize_client()

    # Traitement
    process_file(input_file, chunk_size, file_type, num_threads)
