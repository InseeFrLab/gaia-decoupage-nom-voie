# Montée de version

Sur LS3, il y a régulièrement des montées de version de Python et des versions de packages qui sont bloquées car jugées trop anciennes. Même si on peut revenir sur une ancienne image avec une version ultérieure de Python, il est important de faire les montées de version en temps voulu.

## Stratégie

Les versions les plus récentes de certains packages ne tournent pas sur la dernière version de Python. Pour cela, le mieux est de commencer par les versions les plus anciennes des packages utilisables sur LS3 et monter petit à petit en réglant les conflits jusqu'à arriver à la version qui ne tourne pas. Pour savoir quelles sont les versions disponibles pour un package sur LS3, lancer dans un terminal bash :

```{bash}
pip index versions <nom_du_package>
```

## Modèle NLP

Le modèle NLP utilisé est développé par Spacy mais sont installation est bloquée sur LS3 pour des raisons de sécurité. Pour cela, on va sur la [page web](https://spacy.io/models/fr) du modèle et on télécharge le dossier contenant les informations du modèle **fr_dep_news_trf** via le *Download Link*.  

En mettant le dossier dans un service VScode, on peut l'ouvrir et vérifier qu'il respecte l'architecture de l'ancien modèle. Le dossier doit être un .zip et si c'est un .whl, il suffit de renommer en .zip pour que la conversion se fasse. Il faut aussi penser à changer les configurations qui appellent le modèle : par exemple, si on passe du 3.8.0 au 3.9.0, il faut changer le chemin de fichier dans les settings, le README, le setup.sh etc... (en faisant une recherche dans le code où le chemin de fichier est utilisé, on peut facilement tout changer).  

Il faut placer le dossier .zip dans s3/travail/projet-ml-moteur-identification-gaia/open_data/ sur LS3 et dans s3/projet-gaia/ sur Onyxia (le mettre en public en cliquant sur l'oeil barré à droite du nom de fichier).  

## Conflits

S'il y a des conflits entre packages ou des wheels qui ne tournent pas, se référer aux issues des packages en question sur Git. Souvent, des gens ont déjà rencontré ces problèmes. Soit il existe une solution (ils donnent les versions des packages compatibles), soit il faut baisser la version du package problématique qui ne tourne pas sur la nouvelle version de Python et attendre que le problème se résolve pour monter la version.

