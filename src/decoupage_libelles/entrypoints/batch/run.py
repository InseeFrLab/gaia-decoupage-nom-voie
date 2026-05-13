import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from fastapi.testclient import TestClient

from decoupage_libelles.entrypoints.web.main_api import app, initialize_api
from decoupage_libelles.entrypoints.batch.storage import (
    connect_s3, detect_file_type, iter_chunks, save, output_path
)
from decoupage_libelles.entrypoints.batch.parallel_processor import run_parallel
from decoupage_libelles.config.settings_configuration import settings


# ---------------------------------------------------------------------------
# Lecture de la configuration
# ---------------------------------------------------------------------------


with open(settings.chemin_config) as f:
    config = yaml.load(f, Loader=SafeLoader)

platform = config["platform"]
directory = config["input"]["directory"]
filename = config["input"]["filename"]
sep = config["input"]["sep"]
encoding = config["input"]["encoding"]
output_format = config["output"]["format"]
voie_columns = config["voie_columns"]
chunk_size = config["chunk_size"]
num_threads = config["num_threads"]

# ---------------------------------------------------------------------------
# Construction des chemins
# ---------------------------------------------------------------------------

if platform in ("ls3", "datalab"):
    fs = connect_s3(platform)
    input_file = f"s3://{directory}/{filename}"
else:
    fs = None
    input_file = str(Path(directory) / filename)

file_type = detect_file_type(input_file)
out_path = output_path(input_file, output_format)

# ---------------------------------------------------------------------------
# Initialisation de l'API
# ---------------------------------------------------------------------------

initialize_api()
client = TestClient(app)


def call_api(libelles: list) -> list | None:
    """Appelle l'endpoint de découpage et retourne la liste de résultats."""
    response = client.post("/analyse-libelles-voies", json={"list_labels_voies": libelles})
    if response.status_code != 200:
        print(f"Erreur API : {response.status_code}")
        return None
    return response.json()["reponse"]


# ---------------------------------------------------------------------------
# Traitement
# ---------------------------------------------------------------------------

print(f"Fichier source  : {input_file}")
print(f"Fichier résultat: {out_path}")
print(f"Plateforme      : {platform} — {num_threads} threads — chunks de {chunk_size}")

chunks = iter_chunks(input_file, file_type, chunk_size, fs=fs)
final_df = run_parallel(chunks, None, voie_columns, call_api, num_threads)

save(final_df, out_path, output_format, sep, encoding, fs=fs)
