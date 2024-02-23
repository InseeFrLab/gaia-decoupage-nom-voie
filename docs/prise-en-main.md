
# Prise en main

## Création de l'environnement virtuel

Poetry permet de créer des environnements virtuels : des environnements d'exécution avec des dépendances prédéfinies différement de l'environnement de travail.

Pour définir cet environnement, on utliise le fichier `pyproject.toml` où tout est configuré.

Pour initialiser l'environnement viruel :

```bash
poetry install
```

Cette commande créera un fichier poetry.lock (qu'il faut ajouter à gitignore)

Une fois l'environnement virtuel créé, pour mettre à jour les dépendances associées au fichier `pyproject.toml` :

```bash
poetry update
```

## Lancement de l'application

Pour lancer l'application via l'environnement virutuel exécuter :

```bash
poetry run python src/decoupage_libelles/main2.py
```

## Lancement des tests

```bash
poetry run pytest -v
```