# Lancement du programme

## Installation des dépendances

Les dépendances sont installées dans l'environnement virtuel poetry avec la commande :

```bash
poetry install
```

Le fichier poetry.lock est créé, il ne doit pas être envoyé sur gitlab (il est donc précisé dans .gitignore)

Pour mettre à jour ce fichier, utiliser :

```bash
poetry update
```

## Lancement d'un programme

Pour lancer un programme dans l'environnement virtuel Poetry, utiliser :

```bash
poetry run python nom_du_fichier.py
```

## Lancement des tests

```bash
poetry run python pytest
```

## Génération des dépendances

Pour générer les dépendances et les installer dans l'environnement local, il est possible de jouer les commandes suivantes :

```python
poetry export --output requirements.txt --without-hashes
pip install -r requirements.txt
```


