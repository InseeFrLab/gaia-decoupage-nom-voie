from dynaconf import Dynaconf, Validator
import os

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
settings.chemin_nlp_modele = "../data/fr_dep_news_trf-3.7.0/fr_dep_news_trf/fr_dep_news_trf-3.7.0/"
settings.chemin_type_voie = "../data/type_voie.csv"
settings.chemin_code2lib = "../data/code2lib.json"

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
