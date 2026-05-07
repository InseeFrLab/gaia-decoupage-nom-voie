# Installation et lancement

## Prérequis

Dans son namespace sur Datalab ou LS3, ouvrir un service `Vscode-python` en paramétrant les ressources de cette façon : 
![](data/parametrages_vs_code_decoupage_parallele.png "Paramétrages des ressources du service Vscode")  


## Installation

### Sur LS3
```bash
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies.git
cd gaia-decoupage-libelles-voies/
source ./setup.sh
```

### Sur Datalab
```bash
git clone https://git.lab.sspcloud.fr/scrum-team-gaia/gaia-decoupage.git
cd gaia-decoupage/
wget -P data/ https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.8.0-py3-none-any.zip
pip install -r requirements.txt
unzip data/fr_dep_news_trf-3.8.0-py3-none-any.zip -d data/fr_dep_news_trf-3.8.0/
rm data/fr_dep_news_trf-3.8.0-py3-none-any.zip
cd src/
```

### En local
> ⚠️ Non recommandé pour de gros fichiers.

```bash
git clone https://git.lab.sspcloud.fr/scrum-team-gaia/gaia-decoupage.git
cd gaia-decoupage/
curl -o data/fr_dep_news_trf-3.8.0-py3-none-any.zip https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.8.0-py3-none-any.zip
pip install -r requirements.txt
unzip data/fr_dep_news_trf-3.8.0-py3-none-any.zip -d data/fr_dep_news_trf-3.8.0/
rm data/fr_dep_news_trf-3.8.0-py3-none-any.zip
cd src/
```

## Configuration

Placer le fichier à traiter sur S3 et configurer `src/decoupage_libelles/scripts_parallelises/config.yml` :

| Paramètre | Description | Exemple |
|---|---|---|
| `directory_path` | Dossier S3 du fichier (sans `/` final) | `"travail/projet-ml/confidentiel"` |
| `input_path` | Nom du fichier | `"voies_01.csv"` |
| `output_format` | Format de sortie | `"csv"` ou `"parquet"` |
| `sep` | Séparateur CSV (vide si parquet) | `","` |
| `encodeur` | Encodage CSV (vide si parquet) | `"utf-8"` |
| `vars_names_nom_voie` | Colonne(s) contenant le libellé de voie | `["nom_voie_complet"]` ou `["id_type_voie", "nom_voie_norm"]` |
| `plateform` | Environnement d'exécution | `"ls3"`, `"datalab"` ou `"local"` |

## Lancement

### Sur LS3
```bash
python decoupage_libelles/scripts_parallelises/main.py
```

### Sur Datalab
```bash
nohup python decoupage_libelles/scripts_parallelises/main.py &
```

> Sur Datalab, les logs sont écrits dans `nohup.txt`. Supprimer ce fichier avant chaque nouveau lancement (`rm nohup.txt`).

## Résultat

Le fichier traité est enregistré dans le même dossier S3, avec le même nom suivi de `_parsed`.

Pour livrer en prod, déposer le fichier dans : `\\pd_as_ge_d1_50\ge_data_pd\gaia_pd`.

---

## Arrêter un traitement en cours

### Sur LS3
`Ctrl+Z` dans le terminal. Attendre que le prompt réapparaisse.

### Sur Datalab
```bash
kill <numéro_affiché_au_lancement>   # ex : kill 8371
rm nohup.txt
```

---

## Gestion des fichiers volumineux

### Dézipper un fichier sur LS3

```bash
mc cp s3/projet-gaia/decoupage/ban_2024.zip data/
unzip data/ban_2024.zip -d data/
rm data/ban_2024.zip
# Récupérer le fichier utile
mc cp data/ban_2024/ban_2024.csv s3/projet-gaia/decoupage/
rm -rf data/ban_2024
```

### Télécharger un fichier depuis LS3

```bash
mc cp s3/travail/projet-ml/confidentiel/<fichier> .
tar -czvf <fichier>.tar.gz <fichier>
mc cp <fichier>.tar.gz s3/travail/projet-ml/confidentiel/
```

Télécharger le fichier zippé puis le dézipper deux fois.
