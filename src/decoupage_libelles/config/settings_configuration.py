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
            "chemin_fichier_majic",
            "chemin_referentiel_types_voies",
            "chemin_nlp_modele",
            "chemin_sortie",
            must_exist=True,
            env="default",
        )
    ],
)
# settings.chemin_nlp_modele = "../data/fr_dep_news_trf-3.7.0/fr_dep_news_trf/fr_dep_news_trf-3.7.0/"

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
