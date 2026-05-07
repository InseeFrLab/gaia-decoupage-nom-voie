# Handlers — vue d'ensemble

Les handlers constituent l'arbre de décision principal du découpage. Chaque handler reçoit une liste de voies filtrées par nombre de types détectés, et retourne une liste de `VoieDecoupee`.

## Pipeline commune à tous les handlers

Chaque handler suit le même ordre interne :

```
1. Chercher un complément (BATIMENT, PAVILLON, IMMEUBLE…)
        │
        ├── Complément trouvé → sous-handler "compl"
        │
2. Chercher une voie fictive (RUE A, IMPASSE 3…)
        │
        ├── Voie fictive trouvée → assign_lib_compl
        │
3. Traiter le reste selon la position des types
```

## Les 8 patterns d'assignation possibles

Une fois l'arbre de décision parcouru, l'un des use cases `assign_*` construit le résultat final :

| Pattern | Exemple |
|---|---|
| `lib` | `LES HARDONNIERES` → libellé = "LES HARDONNIERES" |
| `type + lib` | `CHE DES SEMAPHORES` → type = "CHEMIN", lib = "DES SEMAPHORES" |
| `lib + type` | `HOCHE RUE` → type = "RUE", lib = "HOCHE" |
| `type seul` | `GRAND RUE` → type = "GRANDE RUE" |
| `lib + compl` | `LES VERNONS RUE B` → lib = "LES VERNONS", compl = "RUE B" |
| `type + lib + compl` | `RUE HOCHE BAT B` → type = "RUE", lib = "HOCHE", compl = "BAT B" |
| `compl + type + lib` | `BAT A RUE HOCHE` → type = "RUE", lib = "HOCHE", compl = "BAT A" |
| `compl + type + lib + compl` | `HLM AV KLEBER BAT B` → type = "AVENUE", lib = "KLEBER", compl1 = "HLM", compl2 = "BAT B" |

## Routage par nombre de types

```
TypeVoieDecoupageLauncher
        │
        ├── 0 type  ──────────────────► no_type handler
        │
        ├── 1 type  ──────────────────► one_type handler
        │
        └── 2+ types ─────────────────► two_types_and_more handler
                                                │
                                    filtrage NLP (KeepTypesWithoutArticleAdjBefore)
                                                │
                               ┌────────────────┼────────────────┐
                            0 type           1 type           2 types
                               │                │                │
                           assign_lib     one_type handler  two_types handler
```

## Propriétés calculées utilisées par les handlers

Avant de prendre une décision, les handlers s'appuient sur des propriétés calculées par `information_generators/` :

| Propriété | Description |
|---|---|
| `has_type_in_first_pos` | Le premier mot du libellé est un type de voie |
| `has_type_in_second_pos` | Le deuxième mot est un type de voie |
| `has_type_in_last_pos` | Le dernier mot est un type de voie |
| `is_longitudinal` | Type linéaire : RUE, AVENUE, CHEMIN… |
| `is_agglomerant` | Zone d'habitat : RESIDENCE, HLM, HAMEAU… |
| `is_complement` | Type complément : BATIMENT, PAVILLON… |
| `is_escalier_or_appartement` | APPARTEMENT, ESCALIER, BLOC |
| `has_adj_det_before` | Un article/adjectif précède le type (via NLP) |
| `word_after` | Le mot qui suit le type dans le libellé |

## Fichiers concernés

| Handler | Fichier principal |
|---|---|
| 0 type | [`no_type.md`](no_type.md) |
| 1 type | [`one_type.md`](one_type.md) |
| 2 types | [`two_types.md`](two_types.md) |
| 2+ types | [`two_types_and_more.md`](two_types_and_more.md) |
