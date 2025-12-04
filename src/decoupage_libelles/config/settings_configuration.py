from dynaconf import Dynaconf, Validator
import os
from importlib.resources import files
from pathlib import Path

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
            "chemin_types_voies_majic",
            must_exist=True,
            env="default",
        )
    ],
)

root = os.getcwd()

candidate_paths = [
    root + "/fr_dep_news_trf-3.8.0/fr_dep_news_trf/fr_dep_news_trf-3.8.0/",
    root + "/../fr_dep_news_trf-3.8.0/fr_dep_news_trf/fr_dep_news_trf-3.8.0/"
]

for path in candidate_paths:
    if Path(path).exists():
        settings.chemin_nlp_modele = path

# package
settings.chemin_type_voie = files("decoupage_libelles.data").joinpath("type_voie.csv")
settings.chemin_code2lib = files("decoupage_libelles.data").joinpath("code2lib.json")

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
