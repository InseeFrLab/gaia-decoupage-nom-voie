# Handler — 2 types ou plus détectés initialement

**Fichiers** : `handlers/two_types_and_more/usecase/`
- `two_types_and_more_voies_handler_use_case.py`
- `keep_types_without_article_adj_before_use_case.py`

## Contexte

Ce handler est le point d'entrée pour toutes les voies avec 2 types ou plus après la détection initiale. Son rôle est de **réduire** le nombre de types via un filtrage NLP, puis de **rerouter** vers les handlers 1 type ou 2 types selon ce qui reste.

## Pourquoi ce handler existe

Une voie comme `RUE DE LA VALLEE DES ROIS` peut déclencher la détection de `RUE` (type longitudinal) ET `VALLEE` (type agglomerant). Mais `VALLEE` est ici précédé de `DE LA` — ce n'est pas un vrai type de voie, c'est le nom. Le filtrage NLP élimine ces faux positifs avant de router vers le handler approprié.

## Pipeline

```
TwoTypesAndMoreVoiesHandlerUseCase
        │
        ▼ Pour chaque voie :
        │
        ├── SuppressArticleInFirstPlace
        │     Supprime LE/LA/LES si le 1er type est en 2e position
        │
        ├── KeepTypesWithoutArticleAdjBefore  (NLP activé)
        │     Supprime les types précédés d'un article ou adjectif
        │     ex: "DE LA VALLEE" → VALLEE supprimé car précédé de "LA" (DET)
        │     Exceptions : le mot "A" et les mots "DIT"/"DITE" ne déclenchent pas la suppression
        │
        ├── generate_information_on_lib
        │
        └── Routage selon len(types_and_positions) après filtrage
                │
                ├── 0 type → assign_lib
                ├── 1 type → one_type handler
                ├── 2 types → two_types handler
                └── 3+ types → second filtrage (ne garder que long/agglo)
                                        │
                                        ├── 0 type → assign_lib
                                        ├── 1 type → one_type handler
                                        ├── 2 types → two_types handler
                                        └── 3+ types → assign_lib (fallback final)
```

## Second filtrage (3+ types après le premier filtrage NLP)

Si après le filtrage NLP il reste encore 3 types ou plus, un second filtrage plus agressif est appliqué : **seuls les types longitudinaux et agglomerants sont conservés**. Les types "périphériques" (ARCADE, ESPLANADE, JETEE…) sont supprimés.

Listes utilisées :
- `TYPESLONGITUDINAUX2` : ROUTE, BOULEVARD, RUE, AVENUE, IMPASSE, CHEMIN, VOIE, PLACE, CHEMINEMENT, VOIE COMMUNALE, ALLEE
- `TYPESAGGLOMERANTS` : DOMAINE, RESIDENCE, HLM, LOTISSEMENT, HAMEAU, QUARTIER, VILLAGE…

## `KeepTypesWithoutArticleAdjBefore` — détail

Ce use case est utilisé à la fois dans ce handler et dans `HandleOneTypeNotComplNotFictifUseCase` (handler 1 type). Il supprime un type si le mot qui le précède a un postag DET (déterminant) ou ADJ (adjectif) selon le modèle NLP spaCy.

```python
# Règle appliquée pour chaque type non en 1ère position
postag_before = voie.label_postag[position_start - 1]
word_before   = voie.label_preproc[position_start - 1]

if postag_before in POSTAG and word_before != "A" or word_before in ["DIT", "DITE"]:
    # supprimer ce type
```

`POSTAG` = `{"DET", "ADJ"}` (défini dans `PostagBeforeTypeUseCase`).

Le cas `word_before == "A"` est exclu car `A` est souvent une préposition dans les adresses (`RUE A DROITE`), et sa classification NLP comme DET serait un faux positif.

## Asymétrie avec le handler 1 type

Le filtrage NLP est appliqué **en amont** dans ce handler (avant le routage), alors que dans `HandleOneTypeNotComplNotFictifUseCase` il est appliqué **en aval** (après avoir vérifié `has_type_in_first_pos`).

Cette asymétrie est intentionnelle : pour 2+ types, on veut d'abord réduire le bruit avant de décider ; pour 1 type, on peut décider directement si le type est en 1ère position sans avoir besoin du NLP.

## Sorties possibles

Toutes les sorties possibles des handlers one_type et two_types, plus :

| Pattern | Exemple | Condition |
|---|---|---|
| `lib` | `RUE DE LA VALLEE DES ROIS` | Tous les types supprimés par NLP |
| `lib` | Libellé avec 3+ types non réductibles | Fallback final |
