# Construction du livrable

Une distribution Python est une version pré-emballée d'un programme python, simplifiant l'installation et incluant les dépendances utilisées par le programme.

La distribution contient deux fichiers :
- un fichier .tar.gz contenant le code source, le README
- un fichier .whl permettant d'installer les dépendances et de déployer le .tar.gz

Pour créer une distribution, nous allons utiliser poetry.

## Configuration

La configuration de la génération du livrable est dans le fichier `pyproject.toml`, les sections principales sont :

- **tool.poetry.dependencies** contenant la liste des requirements
- **build-system.publish** permettant de définir le lieu où déposer la distribution

## Exécution

```bash
# Installation des requirements
poetry install
# Création de la distribution sous le dossier dist
poetry build
```