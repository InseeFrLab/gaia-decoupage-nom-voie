# Algorithme pour découper type de voie, nom de voie et complément d'adresse à partir d'un libellé de nom de voie brut.

## Getting started

Dans son namespace sur LS3 ou Datalab, ouvrir un service vs-python en paramétrant les ressources de cette façon : 
![](data/parametrages_vs_code_decoupage_parallele.png "Paramétrages des ressources du service vscode")  

Pour utiliser ce code en local (non recommandé), il faudra aller récupérer le dossier contenant le modèle spacy et le mettre dans le dossier data du code. Ce dossier se trouver sur le s3 du Datalab ou LS3 : s3/projet-gaia/fr_dep_news_trf-3.7.0.zip ou s3/travail/projet-ml-moteur-identification-gaia/open_data/fr_dep_news_trf-3.7.0.zip.  

Il faudra se munir de son identifiant GitLab et de son token (associé au projet en question) pour pouvoir cloner le projet.  

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
git clone https://git.lab.sspcloud.fr/scrum-team-gaia/gaia-decoupage.git
cd gaia-decoupage/
source ./setup-datalab.sh
```

En local, lancer l'un des deux scripts, il y aura une erreur pour le "mc cp" qui n'aura pas d'incidence.  

## Lancer le traitement d'un fichier

Placer le fichier dans l'espace de stockage S3, et configurer le fichier src/decoupage_libelles/scripts_parallelises/config.yml :  

- directory_path: Dossier où le fichier à traiter se trouve (Attention, ne pas mettre de "/" à la fin). Ex : "travail/projet-ml-moteur-identification-gaia/confidentiel/personnel_non_sensible".  
- input_path: Nom du fichier. Ex : "voies_01.csv".  
- sep: Si c'est un fichier csv, préciser le séparateur. Ex : ",". Si c'est un parquet, mettre "".  
- encodeur: Si c'est un fichier csv, préciser l'encodeur. Ex : "utf-8". Si c'est un parquet, mettre "".  
- vars_names_nom_voie: Liste de(s) nom(s) de(s) la variable(s) dans laquelle on va extraire le type de voie. Ex : ["nom_voie_complet"] . S'il y a plusieurs à concaténer avec un espace entre chaque, les spécifier dans l'ordre. Ex : ["id_type_voie", "nom_voie_norm"]
- plateform: "ls3", "datalab" ou "local" en fonction de si vous êtes sur LS3, Datalab ou en local.  

### Sur LS3

Dans le terminal bash, lancer :  
```{bash}
python decoupage_libelles/scripts_parallelises/main.py
```

### Sur le Datalab

Dans le terminal bash, lancer :  
```{bash}
nohup python decoupage_libelles/scripts_parallelises/main.py &
```

La commande pour lancer le code sur le Datalab est un peu différente car si le service se met en veille sur le Datalab, le traitement se met en pause. Ceci n'est pas le cas sur LS3. Ici, les log ne se feront pas dans le terminal mais dans le fichier nohup.txt qui se créera dans le code lorsque le découpage sera lancé. Vous pourrez y suivre l'évolution en temps réel. Si vous voulez relancer un nouveau traitement, il faudra supprimer ce fichier nohup.txt pour ne pas réécrire dans l'ancien (en lançant dans le terminal `rm nohup.txt`).

## Récupération du résultat 

Le fichier traité sera enregistré dans le même dossier avec le même format et le même nom de fichier suivi de "_parsed".  

Pour livrer un fichier traité en prod, le placer dans un des dossiers "Livraison" prévu à cet effet sur applishare : "\\pd_as_ge_d1_50\ge_data_pd\gaia_pd". 


## En cas de fichier volumineux

Sur le s3, vous pouvez stocker votre fichier zippé à l'endroit souhaité. Pour le dézipper, il suffit dans un terminal bash de lancer ces commandes :  

```
cd ../
# Le fichier zip est stocké dans le s3 du projet-gaia sur le datalab, dans le dossier "decoupage"
# On va transférer ce fichier zip dans le dossier data du service VSCode
mc cp s3/projet-gaia/decoupage/ban_2024.zip data/
# Le fichier est dézippé dans le dossier data
unzip data/ban_2024.zip -d data/
# Le fichier zippé est supprimé du service VSCode pour ne pas surcharger le service
rm data/ban_2024.zip
```

Ensuite, vous pouvez aller explorer le dossier data dans le service VSCode et repérer ce qu'il vous intéresse. Par exemple, je voudrais récupérer le fichier csv dans le dossier dézippé : 

```
# On met le fichier csv sur le s3 du projet gaia, dans le dossier "decoupage"
mc cp data/ban_2024/ban_2024.csv s3/projet-gaia/decoupage/
# On supprime le dossier dézippé du service VSCode ne pas surcharger
rm -rf data/ban_2024
cd src/
```

Voilà, votre fichier dézippé est bien sur le s3. Vous pouvez lancer un découpage sur ce fichier dès à présent.

## Arrêter un traitement en cours

Dans le terminal, fa