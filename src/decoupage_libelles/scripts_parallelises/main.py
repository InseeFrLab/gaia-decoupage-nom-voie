import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd
import s3fs
from multiprocessing import Pool, cpu_count
import time
from fastapi.testclient import TestClient
import warnings
from decoupage_libelles.entrypoints.web.main_api import app, initialize_api
from tqdm import tqdm
import yaml
from yaml.loader import SafeLoader
import pyarrow.parquet as pq


def initialize_client():
    global client
    client = TestClient(app)


# Fonction de traitement pour chaque chunk
def process_chunk(chunk):
    """
    Fonction qui traite un paquet de données en utilisant le client FastAPI.
    """
    print('Début')

    # Exemple de traitement sur la colonne `nom_voie`
    data = chunk[chunk[var_name_nom_voie].notna()][var_name_nom_voie].tolist()

    if data:
        list_labels_voies = {"list_labels_voies": data}
        print('Lancement du découpage')
        response = client.post("/analyse-libelles-voies", json=list_labels_voies)
        print(response)

        if response.status_code == 200:
            print('Récupération des résultats')
            dict_reponse = response.json()["reponse"]
            rows = []
            for item in dict_reponse:
                for key, value in item.items():
                    row = {"origin": key}
                    row.update(value)
                    rows.append(row)

            df = pd.DataFrame(rows)

        df = df.rename(columns={"origin": var_name_nom_voie})

        merged_df = pd.merge(
            chunk,
            df[[var_name_nom_voie, "typeVoie", "libelleVoie", "complementAdresse", "complementAdresse2"]],
            how="left",
        )

        merged_df.rename(
            columns={
                "typeVoie": "type_voie_parse",
                "libelleVoie": "libelle_voie_parse",
                "complementAdresse": "complement_adresse",
                "complementAdresse2": "complement_adresse2",
            },
            inplace=True,
        )

    return merged_df


def save_dataframes(dfs, file_type):
    """Sauvegarder les DataFrames depuis la queue."""
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.datascience.kube.insee.fr'},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"])

    print("Enregistrement des résultats")
    df_concatenated = pd.concat(dfs, ignore_index=True)

    if file_type == "csv":
        with fs.open(output_file, "wb") as f:
            df_concatenated.to_csv(f, index=False)

    elif file_type == "parquet":
        with fs.open(output_file, "wb") as f:
            df_concatenated.to_parquet(f, engine="pyarrow", index=False)

    print(f"Le fichier traité a été enregistré ici {output_file}")


# Fonction pour lire et traiter un chunk
def process_and_follow_chunk(args):
    """
    Traite et sauvegarde un chunk donné.
    """
    chunk, __ = args
    processed_chunk = process_chunk(chunk)  # Traite le paquet
    return processed_chunk


# Fonction principale pour lire et diviser le fichier en chunks
def process_file_in_chunks(input_file, chunk_size, sep, encodeur, file_type):
    """
    Lit le fichier source en morceaux (chunks) et retourne une liste des chunks avec leur ID.
    """
    results = []
    partition_id = 0
    with fs.open(input_file, "rb") as f:
        if file_type == "csv":
            # Utilisation de tqdm pour afficher une barre de progression
            for chunk in tqdm(pd.read_csv(f, chunksize=chunk_size, sep=sep, encoding=encodeur, dtype=str), desc="Lecture des chunks"):
                results.append((chunk, partition_id))
                partition_id += 1
        elif file_type == "parquet":
            # Utilisation de tqdm pour afficher une barre de progression
            parquet_file = pq.ParquetFile(f)
            for i, batch in tqdm(enumerate(parquet_file.iter_batches(batch_size=chunk_size)), desc="Parsing des voies", unit="chunk"):
                chunk = batch.to_pandas()
                results.append((chunk, partition_id))
                partition_id += 1

    return results


# Main pour exécuter avec multiprocessing
if __name__ == "__main__":  # Variables globales
    start = time.time()
    # Configuration S3
    global fs
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.datascience.kube.insee.fr'},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"])

    with open("decoupage_libelles/scripts_parallelises/config.yml") as f:
        config = yaml.load(f, Loader=SafeLoader)

    s3_bucket = config['s3_bucket']
    input_path = config['input_path']
    input_file = f"s3://{s3_bucket}/{input_path}"
    sep = config["sep"]  # Séparateur CSV
    encodeur = config["encodeur"]
    file_type = input_file.split(".")[1]
    global var_name_nom_voie
    var_name_nom_voie = config['var_name_nom_voie']
    global output_file
    output_file = input_file.split(".")[0] + "_parse." + input_file.split(".")[1]
    chunk_size = 1000  # Taille des paquets à traiter
    num_workers = cpu_count()  # Nombre de processus parallèles

    warnings.filterwarnings("ignore", category=FutureWarning)

    initialize_api()
    initialize_client()

    # Récupérer les chunks à traiter
    chunks_to_process = process_file_in_chunks(input_file, chunk_size, sep, encodeur, file_type)

    global length_chunks_to_process
    length_chunks_to_process = len(chunks_to_process)

    # Initialisation du Pool de multiprocessing
    with Pool(processes=num_workers, initializer=initialize_client) as pool:
        results = pool.map(process_and_follow_chunk, chunks_to_process)

    save_dataframes(results, file_type)
    traitement_time = time.time() - start

    print(f"Traitement et sauvegarde terminés en {round(traitement_time/60)} minutes")
