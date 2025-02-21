# Lancement de l'API

## Pérequis

Créer deux variables d'environnement :

```bash
# Définition du path dans lequel rechercher les modules python
export PYTHONPATH="gaia-decoupage-libelles-voies/src/*"
# Définition du path du chemin de configuration
export SETTINGS_FILE_FOR_DYNACONF="/etc/settings.yaml"
```

## Lancer l'API

```bash
cd gaia-decoupage-libelles-voies
pip install poetry
poetry install
poetry run uvicorn decoupage_libelles.entrypoints.web.main_api:app --port 8000 --reload
```
