# Algorithme pour découper type de voie, nom de voie et complément d'adresse à partir d'un libellé de nom de voie brut.

## Getting started

Installer le package :
```{bash}
pip install decoupage_libelles
```

Exemple d'utilisation du package
```{python}
from decoupage_libelles import decoupe_voies

# Une liste de voies
decoupe_voies(["avenue verdier du bas de la rue", "avenue verdier"])
```

## 📬 Contact

Développé dans le cadre du projet GAIA — Insee.
Auteur : Raya Berova (raya.berova@insee.fr)

## Avec le dépot git

Dans son namespace sur Datalab ou LS3, ouvrir un service vs-python en paramétrant les ressources de cette façon : 
![](data/parametrages_vs_code_decoupage_parallele.png "Paramétrages des ressources du service vscode")  

Il faudra se munir de son identifiant GitLab et de son token (associé au projet en question) pour pouvoir cloner le projet.  

Dans un terminal bash :  

### Sur LS3
```{bash}
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies.git
cd gaia-decoupage-libelles-voies/
source ./setup.sh
```

### Sur Datalab
```{bash}
git clone https://git.lab.sspcloud.fr/scrum-team-gaia/gaia-decoupage.git
cd gaia-decoupage/
cd src/
```

### En local
Attention : ce n'est pas recommandé de lancer ce traitement sur de gros fichiers sur votre ordinateur en local.  
```{bash}
git clone https://github.com/InseeFrLab/gaia-decoupage-nom-voie/
cd gaia-decoupage-nom-voie/
cd src/
```

## Lancer le traitement d'un fichier

Placer le fichier dans l'espace de stockage S3, et configurer le fichier src/decoupage_libelles/scripts_parallelises/config.yml :  

- directory_path: Dossier où le fichier à traiter se trouve (Attention, ne pas mettre de "/" à la fin). Ex : "travail/projet-ml-moteur-identification-gaia/confidentiel/personnel_non_sensible".  
- input_path: Nom du fichier. Ex : "voies_01.csv".
- output_formt: Le format du fichier de sortie. "csv" ou "parquet"
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

Le fichier traité sera enregistré dans le même dossier avec le format choisi et le même nom de fichier suivi de "_parsed".  

Pour livrer un fichier traité en prod, le placer dans un des dossiers "Livraison" prévu à cet effet sur applishare : "\\pd_as_ge_d1_50\ge_data_pd\gaia_pd". 


## En cas de fichier volumineux à mettre sur LS3

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

## En cas de fichier volumineux à télécharger depuis LS3

Dans un service VSCode :

```{bash}
mc cp s3/travail/projet-ml-moteur-identification-gaia/confidentiel/personnel_non_sensible/<fichier_a_zipper> .
tar -czvf <fichier_a_zipper>.tar.gz <fichier_a_zipper>
mc cp <fichier_a_zipper>.tar.gz s3/travail/projet-ml-moteur-identification-gaia/confidentiel/personnel_non_sensible/
```

Télécharger le fichier zippé et le dézipper deux fois d'affilé.


## Arrêter un traitement en cours

### Sur LS3

Dans le terminal, appuyer sur ctrl+Z. Cela peut prendre quelques minutes à s'arrêter, vous saurez que le traitement a été stoppé lorsque vous pourrez réécrire normalement dans le terminal.

### Sur le Datalab

- Copier le numéro qui s'affiche dans le terminal suite au lancement du traitement. Exemple : `[1] 8371`  
- Lancer dans le terminal `kill 8371` pour stopper le traitement.  
- Suppimer le fichier nohup.txt : `rm nohup.txt`.  

