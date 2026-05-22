# Déploiement de l'API avec Kubernetes sur Onyxia

## Déploiement initial

Pour déployer l'API, il faut pusher le code sur un dépot GitHub public afin de construire une image Docker publique.  

Ouvrir un terminal Bash en local (pas sous AUS) dans son Z://.  
Y cloner ce dépot git dans son Z:// : [GitLab interne Insee](https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies).  

```
git clone https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies/
```

Dans le dépot du GitLab interne, rajouter le remote du dépot [GitHub public](https://github.com/InseeFrLab/gaia-decoupage-nom-voie/) :  

```
cd gaia-decoupage-libelles-voies/
git remote add github-remote https://github.com/InseeFrLab/gaia-decoupage-nom-voie/
```

Envoyer les nouveautés de la main du dépot GitLab interne dans le dépot GitHub public :

```
git push github-remote
```

Aller sur le [GitHub public](https://github.com/InseeFrLab/gaia-decoupage-nom-voie/) et voir si le build de l'image Docker a bien fonctionné (dans Actions). Si c'est le cas, alors se rendre sur Onyxia, dans le projet-gaia et ouvrir ArgoCD. Faire New App, Edit as YAML, copier coller [ce template yaml](https://gitlab.insee.fr/geographie/gaia/gaia-decoupage-libelles-voies/-/blob/383119ccb775537de25fee5b8e42b6a8d7d74538/argocd/template-argocd.yaml), Save puis Create.  

L'API est lancée et consultable [ici](https://gaia-decoupage-nom-voie-api.lab.sspcloud.fr/docs).


## Mis à jour de l'API

Mettre à jour les dépot Git interne et public avec git (les mêmes étapes que précédemment). Vérification de la construction effective de l'image. Si c'est bon, il faut synchroniser l'API gaia-decoupage-nom-voie-api sur ArgoCD en appuyant sur Sync.  

L'API est prête !
