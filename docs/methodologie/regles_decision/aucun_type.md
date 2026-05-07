# Handler — 0 type détecté

**Fichiers** : `handlers/no_type/usecase/`
- `no_type_voies_handler_use_case.py`
- `handle_no_type_complement_use_case.py`

## Contexte

Ces voies n'ont aucun type de voie reconnu dans leur libellé. Exemples typiques :
- `LES HARDONNIERES` — nom de lieu-dit sans type
- `LE TILLET BAT A` — complément d'adresse sans type de voie
- `APPARTEMENT JEAN LAMOUR` — appartement identifié par un nom

## Arbre de décision

```
NoTypeVoiesHandlerUseCase
        │
        ▼ Chercher un complément (TYPES_COMPLEMENT_0)
        │  PAVILLON, IMMEUBLE, BATIMENT, BLOC, APPARTEMENT, ESCALIER, LOGEMENT, ENTREE
        │
        ├── Pas de complément
        │       │
        │       └──► assign_lib
        │             ex: "LES HARDONNIERES" → lib = "LES HARDONNIERES"
        │
        └── Complément trouvé → HandleNoTypeComplUseCase
                │
                ▼ NLP activé (apply_nlp_model=True)
                ▼ SuppressArticleInFirstPlace (supprime LE/LA/LES initial)
                ▼ generate_information_on_lib
                │
                ├── Type en position milieu ET pas d'adj/det avant
                │       │
                │       ├── word_after est fictif (A, B, C…) OU is_escalier_or_appartement
                │       │       └──► assign_lib_compl
                │       │             ex: "LE TILLET BAT A" → lib = "LE TILLET", compl = "BAT A"
                │       │
                │       └── word_after non fictif
                │               └──► assign_compl_type_lib
                │                     ex: "LE TILLET BAT ERNEST RENAN"
                │                     → compl = "LE TILLET", type = "BATIMENT", lib = "ERNEST RENAN"
                │
                └── Autre (type en 1ère/dernière pos, ou adj/det avant)
                        │
                        ├── is_escalier_or_appartement
                        │       └──► assign_lib
                        │             ex: "APPARTEMENT JEAN LAMOUR" → lib = "APPARTEMENT JEAN LAMOUR"
                        │
                        └── autre complément (BAT, PAVILLON…)
                                └──► assign_type_lib
                                      ex: "BAT JEAN LAMOUR" → type = "BATIMENT", lib = "JEAN LAMOUR"
```

## Points d'attention

**NLP toujours activé** dans `HandleNoTypeComplUseCase`. C'est le seul handler no_type qui utilise le NLP, car `has_adj_det_before` est indispensable pour distinguer `"LE TILLET BAT ERNEST RENAN"` (complément devant) de `"BAT DE LA FONTAINE"` (article avant BAT → pas un vrai complément).

**`TYPES_COMPLEMENT_0` vs `TYPES_COMPLEMENT_1_2`** : ce handler utilise `TYPES_COMPLEMENT_0`, qui est plus restrictif que la liste utilisée par les handlers 1 et 2 types (ne contient pas `IM`).

## Sorties possibles

| Pattern | Exemple | Condition |
|---|---|---|
| `lib` | `LES HARDONNIERES` | Pas de complément trouvé |
| `lib` | `APPARTEMENT JEAN LAMOUR` | Complément escalier/appart, pas en milieu |
| `lib + compl` | `LE TILLET \| BAT A` | Complément en milieu, word_after fictif |
| `type + lib` | `BAT \| JEAN LAMOUR` | Complément non escalier, pas en milieu |
| `compl + type + lib` | `LE TILLET \| BAT \| ERNEST RENAN` | Complément en milieu, word_after non fictif |
