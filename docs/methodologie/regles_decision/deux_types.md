# Handler — 2 types détectés

**Fichiers** : `handlers/two_types/usecase/`
- `two_types_voies_handler_use_case.py`
- `handle_two_types_complement_use_case.py`
- `handle_two_types_voie_fictive_use_case.py`
- `handle_has_type_in_first_pos_use_case.py`
- `handle_no_type_in_first_pos_use_case.py`
- `compl_first_type_compl_use_case.py`
- `compl_second_type_compl_use_case.py`
- `compl_third_type_compl_use_case.py`
- `compl_two_types_long_or_agglo_use_case.py`

## Contexte

Les cas les plus complexes : le libellé contient deux types reconnus et il faut déterminer lequel est le vrai type de voie, lequel est un complément, et où est le nom de voie.

## Arbre de décision principal

```
TwoTypesVoiesHandlerUseCase
        │
        ▼ Chercher un complément (TYPES_COMPLEMENT)
        │
        ├── Complément trouvé → HandleTwoTypesComplUseCase
        │       │  (cascade, premier use case qui retourne un résultat gagne)
        │       ├── ComplTwoTypesLongOrAgglo
        │       ├── ComplFirstTypeCompl
        │       ├── ComplSecondTypeCompl
        │       ├── ComplThirdTypeCompl
        │       └── assign_lib (fallback)
        │
        ├── Voie fictive (VOIES_FICTIVES_2)
        │       └──► HandleTwoTypesVoieFictive
        │
        └── Reste
                ├── Type en 1ère position → HandleHasTypeInFirstPos
                └── Pas de type en 1ère position → HandleNoTypeInFirstPos
```

## Cas avec complément — cascade de 4 use cases

### `ComplTwoTypesLongOrAgglo`

Traite les cas où parmi les 3 types (2 détectés + 1 complément), on identifie un schéma agglomerant/longitudinal clair.

```
├── 1er agglo + 2e longitudinal
│       └──► compl + 2e type + lib + 3e type compl
│             ex: "HLM AV KLEBER BAT DESCARTES"
├── (1er agglo OU 2e agglo) + 3e longitudinal
│       └──► compl + 3e type + lib
│             ex: "HLM BAT DESCARTES AV KLEBER"
├── 1er longitudinal + (2e agglo OU 3e agglo)
│       └──► 1er type + lib + compl
│             ex: "RUE HOCHE HLM BAT DESCARTES"
└── (2e agglo + 3e agglo) OU (2e long + 3e long) OU (2e long + 3e agglo)
        └──► compl + 2e type + lib + 3e compl
              ex: "IMM BLEU RUE DES LYS RESIDENCE ERNEST RENAN"
```

### `ComplFirstTypeCompl`

Le 1er type est un complément.

```
├── Type en 1ère ET 2e pos → assign_type_lib avec le 1er type   ex: "LDT VAL DES PINS"
├── 2e type longitudinal/agglomerant → compl + 2e type + lib
├── 3e type longitudinal/agglomerant → compl + 3e type + lib
└── Aucun longitudinal/agglomerant → lib
```

### `ComplSecondTypeCompl`

Le 2e type est un complément.

```
▼ NLP activé si besoin
├── 1er long/agglo + 3e non long/agglo
│       ├── adj/det avant le 2e → 1er type + lib
│       └── pas adj/det → 1er type + lib + compl
├── 3e long/agglo + 1er non long/agglo → compl + 3e type + lib
└── Autre → lib
```

### `ComplThirdTypeCompl`

Le 3e type est un complément.

```
├── 1er long/agglo + 2e non long/agglo → 1er type + lib + 3e type compl
│       ex: "RUE DU CHATEAU BAT BLEU"
└── Autre → lib
```

## Cas voie fictive

```
HandleTwoTypesVoieFictive
        │
        ├── Distance entre les 2 types > 2 mots
        │       └──► 1er type + lib + compl
        │             ex: "RESIDENCE ERNEST RENAN RUE A"
        ├── 1 mot entre les 2 types, longueur 1 (une lettre)
        │       └──► compl + 2e type + lib
        │             ex: "RUE A RESIDENCE ERNEST RENAN"
        └── Autre
                └──► 1er type + lib + compl
                      ex: "RESIDENCE SOLEIL RUE A"
```

## Cas général — type en 1ère position (`HandleHasTypeInFirstPos`)

C'est le sous-cas le plus riche. Il utilise `COMBINAISONS_LONG`, un dictionnaire de 55 paires de types qui détermine lequel des deux prend la priorité.

```
├── 2e type en 2e ou dernière pos
│       ├── 2e type en dernière pos + nom canonique exact
│       │       ├── combinaison dans COMBINAISONS_LONG → last_type_prio ?
│       │       │       ├── oui (2e prioritaire) → lib + dernier type
│       │       │       └── non (1er prioritaire) → 1er type + lib
│       │       └── 1er type non canonique OU non long/agglo OU 2e prioritaire
│       │               └──► lib + dernier type
│       └── 2e type non en dernière pos → 1er type + lib
│
└── 2e type en milieu
        ├── 2e non long/agglo → 1er type + lib   ex: "RUE DU CHATEAU"
        ├── 1er non long + 2e long → compl + 2e type + lib
        │       ex: "CHATEAU DE VERSAILLES RUE HOCHE"
        ├── 1er agglo + 2e long → compl + 2e type + lib
        │       ex: "RESIDENCE VINCENNES RUE HOCHE"
        ├── 2 longs
        │       ├── mêmes types → lib   ex: "RUE HOCHE RUE VERDIER"
        │       ├── dans COMBINAISONS_LONG, 2e prioritaire → compl + 2e + lib
        │       └── 1er prioritaire → 1er type + lib + compl
        ├── 2 agglos
        │       ├── mêmes types → lib
        │       ├── 2e = RESIDENCE ou HLM → compl + 2e type + lib
        │       └── autre → 1er type + lib + compl
        └── 1er long + 2e agglo → 1er type + lib + compl
                ex: "RUE HOCHE RESIDENCE ERNEST RENAN"
```

### La table `COMBINAISONS_LONG`

Exemples de règles :

| Combinaison | Valeur | Signification |
|---|---|---|
| `RUE/ROUTE` | `True` | RUE prioritaire sur ROUTE |
| `ROUTE/RUE` | `False` | RUE (2e) prioritaire sur ROUTE (1er) |
| `CHEMIN/RUE` | `False` | RUE (2e) prioritaire sur CHEMIN (1er) |
| `RUE/CHEMIN` | `True` | RUE (1er) prioritaire sur CHEMIN (2e) |

> Si une combinaison est absente du dictionnaire, le code tombe dans le cas par défaut (`1er type + lib`). Un warning est loggé. Voir [contributing.md](../../contributing.md) pour ajouter une règle.

## Cas général — pas de type en 1ère position (`HandleNoTypeInFirstPos`)

```
├── Type en dernière pos + nom canonique exact → lib + dernier type
├── Aucun long/agglo → lib
├── 1er long/agglo + 2e non → compl + 1er type + lib
│       ex: "VERDIER RESIDENCE DE LA FONTAINE VERTE"
├── 1er non + 2e long/agglo → lib
└── Les deux long/agglo
        ├── 1er longitudinal → compl + 1er type + lib + compl
        │       ex: "VERDIER RUE HOCHE RESIDENCE SOLEIL"
        └── 1er agglomerant → compl + 2e type + lib
                ex: "VERDIER RESIDENCE SOLEIL RUE HOCHE"
```
