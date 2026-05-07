# Handler — 1 type détecté

**Fichiers** : `handlers/one_type/usecase/`
- `one_type_voies_handler_use_case.py`
- `handle_one_type_complement_use_case.py`
- `handle_one_type_not_compl_not_fictif_use_case.py`
- `compl_type_in_first_or_second_pos_use_case.py`
- `compl_type_in_first_or_last_pos_use_case.py`
- `compl_type_in_first_or_middle_pos_use_case.py`

## Contexte

La grande majorité des voies. Le type est détecté et il faut déterminer si le reste du libellé est un nom de voie simple, ou s'il contient un complément d'adresse.

## Prétraitement systématique

Avant tout routage, pour chaque voie :
1. `SuppressArticleInFirstPlace` — supprime `LE`/`LA`/`LES` si le type est en 2e position.
2. `generate_information_on_lib(apply_nlp_model=False)` — calcule les positions du type (1ère, 2e, dernière).

Le NLP n'est activé que dans certains sous-cas, là où `has_adj_det_before` est nécessaire.

## Arbre de décision

```
OneTypeVoiesHandlerUseCase
        │
        ▼ Chercher un complément (TYPES_COMPLEMENT_1_2)
        │
        ├── Complément trouvé → HandleOneTypeComplUseCase
        │       │
        │       ├── Type en 1ère position
        │       │       ├── type aussi en 2e pos → ComplTypeInFirstOrSecondPos
        │       │       ├── type aussi en dernière pos → ComplTypeInFirstOrLastPos
        │       │       └── type en milieu → ComplTypeInFirstOrMiddlePos
        │       │
        │       ├── Type en dernière pos ET pas complément
        │       │       ▼ NLP activé
        │       │       ├── nom canonique exact ET pas adj/det avant
        │       │       │       └──► assign_lib_type   ex: "PO IMM RUE" → lib="PO IMM", type="RUE"
        │       │       └── autre → assign_lib
        │       │
        │       └── Autre → assign_lib
        │               ex: "BEAU PAVILLON DE LA FORET" → lib = "BEAU PAVILLON DE LA FORET"
        │
        ├── Voie fictive (VOIES_FICTIVES_1)
        │       └──► assign_lib_compl
        │             ex: "LES VERNONS RUE B" → lib = "LES VERNONS", compl = "RUE B"
        │
        └── Reste → HandleOneTypeNotComplNotFictifUseCase
                │
                ▼ generate_information_on_lib(apply_nlp_model=False)
                │
                ├── Type en 1ère position
                │       ├── type aussi en dernière pos (seul type dans le libellé)
                │       │       └──► assign_type   ex: "GRAND RUE" → type = "GRANDE RUE"
                │       └── type non en dernière pos
                │               └──► assign_type_lib   ex: "CHE DES SEMAPHORES"
                │
                └── Type non en 1ère position → KeepTypesWithoutArticleAdjBefore (NLP)
                        │
                        ├── 1 type restant, nom canonique exact, en dernière pos
                        │       └──► assign_lib_type   ex: "HOCHE RUE"
                        │
                        ├── 1 type restant, longitudinal/agglomerant, pas en dernière pos
                        │       └──► assign_compl_type_lib
                        │             ex: "LE BAS FAURE RUE DE TOUL"
                        │
                        ├── 1 type restant, longitudinal/agglomerant, en dernière pos
                        │       └──► assign_lib_type   ex: "HOCHE RUE"
                        │
                        └── Autre (type précédé d'un article/adjectif, donc faux positif)
                                └──► assign_lib
```

## Détail des sous-cas avec complément

### `ComplTypeInFirstOrSecondPos` — type en 1ère ET 2e position

Le libellé commence par deux types consécutifs. Exemples : `IMM RESIDENCE BERYL`, `LDT VAL DES PINS`.

```
├── 1er type = complément ET (immeuble + 2e type dans TYPES_COMPLEMENT_IMMEUBLE)
│       └──► assign_type_lib avec le 2e type   ex: "IMM RESIDENCE BERYL" → type="RESIDENCE"
├── 1er type = complément, is_escalier_or_appartement
│       └──► assign_lib   ex: "APPARTEMENT VAL D'ILLAZ"
├── 1er type = complément, autre
│       └──► assign_type_lib avec le 1er type
└── 2e type = complément
        └──► assign_type_lib avec le 1er type   ex: "VC PAVILLON LA PALUN"
```

### `ComplTypeInFirstOrLastPos` — type en 1ère ET dernière position

```
▼ NLP activé
├── 1er type = complément, is_escalier_or_appartement
│       └──► assign_lib   ex: "APPARTEMENT LE PARC"
├── 1er type = complément, 2e type = nom canonique exact ET pas adj/det avant
│       └──► assign_lib_type avec le 2e type   ex: "IMM SOLEIL RUE"
├── 1er type = complément, autre
│       └──► assign_type_lib avec le 1er type   ex: "IMM LE PARC"
└── 2e type = complément
        └──► assign_type_lib avec le 1er type   ex: "IMP DU PAVILLON"
```

### `ComplTypeInFirstOrMiddlePos` — type en 1ère position, complément en milieu

```
▼ NLP activé
├── 1er type = complément
│       ├── pas d'adj/det avant le 2e type
│       │       └──► assign_compl_type_lib avec le 2e type
│       │             ex: "BAT L'ANJOU AV DE VLAMINCK"
│       ├── adj/det avant le 2e type, is_escalier_or_appartement
│       │       └──► assign_lib
│       └── adj/det avant le 2e type, autre complément
│               └──► assign_type_lib avec le 1er type
└── 2e type = complément
        ├── pas d'adj/det avant
        │       └──► assign_type_lib_compl   ex: "HLM LES CHARTREUX BAT B2"
        └── adj/det avant
                └──► assign_type_lib avec le 1er type   ex: "RUE DU PAVILLON DE LA MARINE"
```

## Sorties possibles

| Pattern | Exemple |
|---|---|
| `lib` | `LES HARDONNIERES`, `BEAU PAVILLON DE LA FORET` |
| `type seul` | `GRAND RUE` |
| `type + lib` | `CHE DES SEMAPHORES` |
| `lib + type` | `HOCHE RUE` |
| `lib + compl` | `LES VERNONS RUE B` |
| `type + lib + compl` | `HLM LES CHARTREUX BAT B2` |
| `compl + type + lib` | `BAT L'ANJOU AV DE VLAMINCK` |
