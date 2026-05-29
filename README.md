# gaia-decoupage-libelles-voies

Algorithme de découpage d'un libellé de voie brut en **type de voie**, **nom de voie** et **complément d'adresse**.

## Lancement rapide

```bash
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies.git
cd gaia-decoupage-libelles-voies/
source ./setup.sh
```

### Découpage de voie unitaire

```bash
python -m decoupage_libelles.main "rue hoche"
```

### Un fichier stocké sur LS3
Modifier `config.yml` à la racine, puis lancer :

```bash
python -m decoupage_libelles.entrypoints.batch.run
```

### Détection de type de voie unitaire

```bash
python -m decoupage_libelles.main_detect_type "rue hoche"
```

### Application du modèle NLP unitaire

```bash
python -m decoupage_libelles.main_nlp "rue hoche"
```

## Documentation

| Document | Description |
|---|---|
| [Installation et lancement](docs/getting_started.md) | Cloner, configurer, lancer sur LS3 / Datalab / local |
| [Architecture du code](docs/architecture.md) | Structure des dossiers et rôle de chaque module |
| [Contribuer](docs/comment_contribuer.md) | Ajouter des synonymes, modifier des règles de détection |

### Documentation technique détaillée

| Document | Description |
|---|---|
| [Détection du type de voie](docs/methodologie/detection_type_voie.md) | Pipeline find_type étape par étape |
| [Handlers — vue d'ensemble](docs/methodologie/regles_decision/idee_globale.md) | Arbre de décision et patterns d'assignation |
| [Handler 0 type](docs/methodologie/regles_decision/aucun_type.md) | Voies sans type reconnu |
| [Handler 1 type](docs/methodologie/regles_decision/un_type.md) | Voies avec un seul type (cas majoritaire) |
| [Handler 2 types](docs/methodologie/regles_decision/deux_types.md) | Voies avec deux types détectés |
| [Handler 2+ types](docs/methodologie/regles_decision/plus_de_deux_types.md) | Filtrage NLP et reroutage |
