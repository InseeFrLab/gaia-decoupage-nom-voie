from dynaconf import Dynaconf, Validator
import os
from importlib.resources import files
from pathlib import Path
import subprocess


def install_model(destination: str = "fr_dep_news_trf-3.8.0", use_intranet: bool = False):
    """
    Télécharge et décompresse le modèle NLP nécessaire.

    Args:
        destination: chemin où installer le modèle
        use_intranet: True si téléchargement depuis Nexus interne, False depuis internet
    """
    dest_path = Path(destination)
    if dest_path.exists():
        return dest_path / "fr_dep_news_trf" / "fr_dep_news_trf-3.8.0"

    if use_intranet:
        url = "https://nexus.insee.fr/repository/huggingface-hosted/spacy/fr_dep_news_trf/model.tar.gz"
        tar_path = dest_path / "model.tar.gz"
        dest_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", url, "--output", str(tar_path)], check=True)
        subprocess.run(["tar", "-xzf", str(tar_path), "-C", str(dest_path)], check=True)
        tar_path.unlink()
    else:
        url = "https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.8.0-py3-none-any.zip"
        zip_path = Path(".") / "fr_dep_news_trf-3.8.0-py3-none-any.zip"
        subprocess.run(["wget", "-P", ".", url], check=True)
        subprocess.run(["unzip", str(zip_path), "-d", str(dest_path)], check=True)
        zip_path.unlink()

    return dest_path / "fr_dep_news_trf" / "fr_dep_news_trf-3.8.0"


dest_path = install_model()

SETTINGS_FILE_FOR_DYNACONF = os.environ.get(
    "SETTINGS_FILE_FOR_DYNACONF",
    ["settings.yaml"],
)

settings = Dynaconf(
    envvar_prefix="FIGARO",
    settings_files=SETTINGS_FILE_FOR_DYNACONF,
    environments=False,
    Validators=[
        # valide que les elements de configuration sont bien renseignés
        Validator(
            "chemin_nlp_modele",
            "chemin_types_voies",
            "chemin_code2lib",
            must_exist=True,
            env="default",
        )
    ],
)

root = os.getcwd()

settings.chemin_nlp_modele = str(dest_path)

# package
settings.chemin_type_voie = files("decoupage_libelles.data").joinpath("type_voie.csv")
settings.chemin_code2lib = files("decoupage_libelles.data").joinpath("code2lib.json")

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
