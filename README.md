# Algorithme pour découper type de voie, nom de voie et complément d'adresse à partir d'un libellé de nom de voie brut.

## Getting started

Dans son namespace sur LS3 ou Datalab, ouvrir un service vs-python en paramétrant les ressources de cette façon : 
![](data/parametrages_vs_code_decoupage_parallele.png "Paramétrages des ressources du service vscode")  

Pour utiliser ce code en local (non recommandé), il faudra aller récupérer le dossier contenant le modèle spacy et le mettre dans le dossier data du code. Ce dossier se trouver sur le s3 du Datalab ou LS3 : s3/projet-gaia/fr_dep_news_trf-3.7.0.zip ou s3/travail/projet-ml-moteur-identification-gaia/open_data/fr_dep_news_trf-3.7.0.zip.  

Il faudra se munir de son identifiant GitLab et de son token pour pouvoir cloner le projet.  

### Sur LS3
Lancer dans un terminal bash : 
```{bash}
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies.git
cd gaia-decoupage-libelles-voies/
source ./setup-ls3.sh
```

### Sur Datalab
Lancer dans un terminal bash : 
```{bash}
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies.git
cd gaia-decoupage-libelles-voies/
source ./setup-datalab.sh
```

En local, lancer l'un des deux scripts, il y aura une erreur pour le "mc cp" qui n'aura pas d'incidence.  

## Lancer le traitement d'un fichier

Placer le fichier dans l'espace de stockage S3, et configurer le fichier src/decoupage_libelles/scripts_parallelises/config.yml :  

- directory_path: Dossier où le fichier à traiter se trouve. Ex : "travail/projet-ml-moteur-identification-gaia/confidentiel/personnel_non_sensible".  
- input_path: Nom du fichier. Ex : "voies_01.csv".  
- sep: Si c'est un fichier csv, préciser le séparateur. Ex : ",". Si c'est un parquet, mettre "".  
- encodeur: Si c'est un fichier csv, préciser l'encodeur. Ex : "utf-8". Si c'est un parquet, mettre "".  
- vars_names_nom_voie: Liste de(s) nom(s) de(s) la variable(s) dans laquelle on va extraire le type de voie. Ex : ["nom_voie_complet"] . S'il y a plusieurs à concaténer avec un espace entre chaque, les spécifier dans l'ordre. Ex : ["id_type_voie", "nom_voie_norm"]
- plateform: "ls3", "datalab" ou "local" en fonction de si vous êtes sur LS3, Datalab ou en local.  

Dans le terminal bash, lancer :  
```{bash}
python decoupage_libelles/scripts_parallelises/main.py
```

Le fichier traité sera enregistré dans le même dossier avec le même format et le même nom de fichier suivi de "_parsed".  

Pour livrer un fichier traité en prod, le placer dans un des dossiers "Livraison" prévu à cet effet sur applishare : "\\pd_as_ge_d1_50\ge_data_pd\gaia_pd". 
