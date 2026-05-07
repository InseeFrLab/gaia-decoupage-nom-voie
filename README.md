# gaia-decoupage-libelles-voies

Algorithme de découpage d'un libellé de voie brut en **type de voie**, **nom de voie** et **complément d'adresse**.

## Documentation

| Document | Description |
|---|---|
| [Installation et lancement](docs/getting_started.md) | Cloner, installer et lancer un traitement |
| [Pipeline find_type](docs/find_type.md) | Fonctionnement détaillé de la détection du type de voie |

## Lancement rapide

```bash
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies.git
cd gaia-decoupage-libelles-voies/
source ./setup.sh
python decoupage_libelles/scripts_parallelises/main.py
```

> Voir [docs/getting_started.md](docs/getting_started.md) pour les instructions complètes (Datalab, local, fichiers volumineux).
