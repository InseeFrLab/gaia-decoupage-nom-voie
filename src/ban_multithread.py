import pandas as pd
import s3fs
from multiprocessing import Pool, cpu_count
import os
import time
from fastapi.testclient import TestClient
import warnings
from decoupage_libelles.entrypoints.web.main_api import app, initialize_api
from tqdm import tqdm


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

        merged_df["code_insee"] = merged_df["code_insee"].astype(str).str.zfill(5)
        merged_df["code_postal"] = merged_df["code_postal"].astype(str).str.zfill(5)

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


def save_dataframes(dfs):
    """Sauvegarder les DataFrames depuis la queue."""
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.datascience.kube.insee.fr'},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"])

    print(f"Enregistrement des résultats")
    df_concatenated = pd.concat(dfs, ignore_index=True)
    with fs.open(output_file, "wb") as f:
        df_concatenated.to_parquet(f, engine="pyarrow", index=False)


# Fonction pour lire et traiter un chunk
def process_and_follow_chunk(args):
    """
    Traite et sauvegarde un chunk donné.
    """
    chunk, __ = args
    processed_chunk = process_chunk(chunk)  # Traite le paquet
    return processed_chunk


# Fonction principale pour lire et diviser le fichier en chunks
def process_file_in_chunks(input_file, chunk_size, sep, encodeur):
    """
    Lit le fichier source en morceaux (chunks) et retourne une liste des chunks avec leur ID.
    """
    results = []
    partition_id = 0

    with fs.open(input_file, "rb") as f:
        # Utilisation de tqdm pour afficher une barre de progression
        for chunk in tqdm(pd.read_csv(f, chunksize=chunk_size, sep=sep, encoding=encodeur, dtype=str), desc="Lecture des chunks"):
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

    s3_bucket = "travail/user-fi7l7t/confidentiel/personnel_non_sensible"
    input_file = f"s3://{s3_bucket}/adresses_ban_2024-06-01.csv"
    global output_file
    output_file = f"s3://{s3_bucket}/adresses_ban_2024-06-01_parse.parquet"
    chunk_size = 100_000  # Taille des paquets à traiter
    sep = ";"  # Séparateur CSV
    encodeur = "utf-8"
    num_workers = cpu_count()  # Nombre de processus parallèles
    global var_name_nom_voie
    var_name_nom_voie = "nom_voie"

    warnings.filterwarnings("ignore", category=FutureWarning)

    initialize_api()
    initialize_client()

    # Récupérer les chunks à traiter
    chunks_to_process = process_file_in_chunks(input_file, chunk_size, sep, encodeur)

    global length_chunks_to_process
    length_chunks_to_process = len(chunks_to_process)

    # Initialisation du Pool de multiprocessing
    with Pool(processes=num_workers, initializer=initialize_client) as pool:
        results = pool.map(process_and_follow_chunk, chunks_to_process)

    save_dataframes(results)
    traitement_time = time.time() - start

    print(f"Traitement et sauvegarde terminés en {round(traitement_time/60)} minutes")
