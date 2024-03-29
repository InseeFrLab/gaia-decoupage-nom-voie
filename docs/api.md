# Mise en place de l'api

## Outils utilisés

* **FastAPI** : Framework de création d'API web avec Python.
* **Uvicorn** : Serveur ASGI utilisé pour exécuter l'application FastAPI.

Les dépendances sont ajoutées au fichier `pyproject.toml` pour être utilisables avec poetry.

## Lancement du service

```bash
poetry run uvicorn decoupage_libelles.entrypoints.web.main_api:app --port 8000 --reload
```

L'application est ensuite accessible à l'url :  http://localhost:8000

Par défaut, un Swagger est disponnible à l'adresse :  http://localhost:8000/docs, une redirection a été faite pour que le Swagger soit accessible à la racine de l'API.

## Fonctionnement

Le démarrage et l'appel de l'API sont gérés dans  `src/decoupage_libelles/entrypoints/web/main_api.py``

La méthode `initialize_api()` est appelée au démarrage de l'API, elle doit contenir :

- Le chargement des données
- L'intialisation du modèle

La méthode `analyse_libelles_voies()` permet de définir l'url http://localhost:8000/analyse-libelles-voies appelée avec la méthode POST et un body : {"libelle": "libelle"} renvoi :

```json
{
    "reponse": {
        "libelle": "libelle"
    }
}
```
