# Documentation du pipeline `find_type`

## Vue d'ensemble

Le pipeline `find_type` détecte le **type de voie** (ex : `AVENUE`, `CHEMIN`, `ANCIEN CHEMIN`) dans un libellé d'adresse prétraité, et retourne sa position dans le libellé.

```
Adresse brute
    │
    ▼
PonctuationPreprocessorUseCase   ← étape amont, avant find_type
    │  - mise en majuscules, suppression ponctuation
    │  - dilatation des synonymes extras (ST→SAINT, DR→DOCTEUR…)
    │  → produit label_preproc : ["SAINT", "AVENUE", "VICTOR", "HUGO"]
    │
    ▼
TypeFinderUseCase                ← orchestrateur principal
    │
    ├─ 1. DetectTypesUseCase
    ├─ 2. UpdateOccurrencesByOrderUseCase   ┐ seulement si
    ├─ 3. RemoveDuplicatesUseCase           │ plusieurs types
    └─ 4. RemoveWrongDetectionsUseCase      ┘ détectés
```

---

## Données de référence

### `type_voie_synonyms.csv`

Fichier source unique, chargé au démarrage dans `TypeFinderUtils`.

| LIBELLE_CANONIQUE | VARIANTE     | MAJIC | BAN  | RCA  |
|-------------------|--------------|-------|------|------|
| AVENUE            | AV           | True  | True | True |
| AVENUE            | AVE          | True  | True | True |
| AVENUE            | AVENUE       | True  | True | True |
| CHEMIN            | CHE          | True  | True | True |
| CHEMIN            | CHEMIN       | True  | True | True |
| ANCIEN CHEMIN     | ANC CHEM     | True  | True | True |
| ANCIEN CHEMIN     | ANCIEN CHEMIN| True  | True | True |

Chaque ligne associe une **variante** (toutes les façons d'écrire un type) à son **libellé canonique** (la forme longue de référence retournée en sortie).

> **Important** : les lignes `AVENUE/AVENUE`, `CHEMIN/CHEMIN` etc. sont dans le CSV — c'est la source de vérité, pas le code.

---

## Étape 0 — `GenerateTypeFinderUtilsUseCase` (initialisation)

**Quand ?** Une seule fois au démarrage, pas à chaque adresse.

**Ce que ça fait :**

1. Lit le CSV → extrait les `canoniques` uniques (`{"AVENUE", "CHEMIN", …}`)
2. Pour chaque variante du CSV, applique `PonctuationPreprocessorUseCase` (même prétraitement que l'adresse) pour obtenir la forme normalisée
3. Construit deux dictionnaires :
   - `variante2canonique` : `{"AV": "AVENUE", "AVE": "AVENUE", "AVENUE": "AVENUE", "ANC CHEM": "ANCIEN CHEMIN", …}`
   - `variante2preproc` : `{"AV": "AV", "ANC CHEM": "ANC CHEM", …}`
4. Sépare les variantes en deux listes :
   - `variantes_mono` : variantes d'un seul mot (`["AV", "AVE", "AVENUE", "CHE", …]`)
   - `variantes_multi` : variantes de plusieurs mots (`["ANC CHEM", "ANCIEN CHEMIN", …]`)

> **Pourquoi séparer mono et multi ?** Pour optimiser la recherche : les variantes mono-mots sont cherchées par lookup direct dans une liste, les multi-mots par recherche de sous-séquence.

---

## Étape 1 — `DetectTypesUseCase`

**Entrée :** `label_preproc = ["ABE", "ABBAYE", "DES", "PINS"]`

**Ce que ça fait :**

**Variantes mono-mot** — recherche directe mot à mot :
```
Pour chaque variante mono connue (ex: "ABE", "ABBAYE", "AV"…) :
    Si la variante est dans label_preproc :
        → enregistrer la position et le canonique correspondant
```

**Variantes multi-mots** — recherche de sous-séquence :
```
Pour chaque variante multi connue (ex: "ANC CHEM", "ANCIEN CHEMIN"…) :
    Si la variante apparaît comme chaîne dans label_preproc :
        → vérifier mot par mot la sous-séquence exacte
        → enregistrer la position et le canonique
```

**Sortie pour `"ABE ABBAYE DES PINS"` :**
```python
types_and_positions = {
    ("ABBAYE", 1): (0, 0),   # ABE en position 0
    ("ABBAYE", 2): (1, 1),   # ABBAYE en position 1
}
```

> **Note :** les occurrences sont numérotées 1, 2… dans l'ordre de détection, pas forcément dans l'ordre d'apparition dans le libellé — c'est corrigé à l'étape suivante.

---

## Étape 2 — `UpdateOccurrencesByOrderUseCase`

**Seulement si** plusieurs types ont été détectés.

**Ce que ça fait :** trie les types par position d'apparition dans le libellé et renumérote les occurrences en conséquence.

**Exemple :**
```python
# Avant (ordre de détection)
{("AVENUE", 1): (3, 3), ("RUE", 1): (0, 0)}

# Après (ordre d'apparition)
{("RUE", 1): (0, 0), ("AVENUE", 1): (3, 3)}
```

---

## Étape 3 — `RemoveDuplicatesUseCase`

**Seulement si** plusieurs types ont été détectés.

**Problème traité :** quand une variante courte et sa forme longue apparaissent côte à côte dans le libellé et pointent vers le même canonique.

**Exemple :** `ABE ABBAYE` → `ABBAYE` est détecté deux fois (via `ABE` et via `ABBAYE`)

```python
types_and_positions = {
    ("ABBAYE", 1): (0, 0),  # ABE — 1 mot
    ("ABBAYE", 2): (1, 1),  # ABBAYE — 1 mot
}
```

**Règle :** si deux occurrences du même canonique sont **adjacentes** (`pos2[0] - pos1[1] == 1`), on supprime la plus courte et on retire ses mots du `label_preproc`.

**Sortie :**
```python
label_preproc = ["ABBAYE", "DES", "PINS"]   # ABE retiré
types_and_positions = {
    ("ABBAYE", 1): (0, 0),   # seule occurrence restante
}
```

---

## Étape 4 — `RemoveWrongDetectionsUseCase`

**Seulement si** plusieurs types ont été détectés.

**Problème traité :** quand deux types **différents** sont détectés, mais que l'un est contenu dans le nom de l'autre — c'est donc un faux positif.

**Deux sous-cas :**

### Cas 1 — le court est **inclus dans le span** du long

Exemple : `ANC CHEM DES PINS`
- `CHEMIN` détecté en position `(1, 1)` via le mot `CHEM`
- `ANCIEN CHEMIN` détecté en positions `(0, 1)` via `ANC CHEM`

`CHEMIN` est dans le nom `ANCIEN CHEMIN`, et son span `(1,1)` est à l'intérieur du span `(0,1)` → faux positif.

**Action :** supprimer `CHEMIN` du dict, **sans** retirer de mots du `label_preproc` (les mots appartiennent au type long).

```python
# Avant
{("CHEMIN", 1): (1, 1), ("ANCIEN CHEMIN", 1): (0, 1)}

# Après
{("ANCIEN CHEMIN", 1): (0, 1)}
```

### Cas 2 — le court est **adjacent** au long

Exemple : `ROUTE ANCIENNE ROUTE BIDULE`
- `ROUTE` détecté en `(0, 0)`
- `ANCIENNE ROUTE` détecté en `(1, 2)`

`ROUTE` est dans le nom `ANCIENNE ROUTE`, et son span colle au span du long (`1 - 0 == 1`) → faux positif.

**Action :** supprimer `ROUTE` du dict **et** retirer le mot du `label_preproc` (le mot `ROUTE` en position 0 ne fait pas partie du type long).

```python
# Avant
label_preproc = ["ROUTE", "ANCIENNE", "ROUTE", "BIDULE"]
{("ROUTE", 1): (0, 0), ("ANCIENNE ROUTE", 1): (1, 2)}

# Après
label_preproc = ["ANCIENNE", "ROUTE", "BIDULE"]
{("ANCIENNE ROUTE", 1): (0, 1)}   # positions décalées
```

---

## `RemoveTypeFromLibUseCase` (outil partagé)

Utilisé par les étapes 3 et 4 pour retirer physiquement des mots du `label_preproc`.

**Ce que ça fait :**
1. Supprime les mots entre `pos_start` et `pos_end` de `label_preproc`
2. Décale toutes les positions enregistrées dans `types_and_positions` qui se trouvent après la suppression

---

## Résumé du pipeline complet

```
"ABE ABBAYE DES PINS"
        │
        ▼ PonctuationPreprocessorUseCase
label_preproc = ["ABE", "ABBAYE", "DES", "PINS"]
        │
        ▼ DetectTypesUseCase
types_and_positions = {("ABBAYE", 1): (0,0), ("ABBAYE", 2): (1,1)}
        │
        ▼ UpdateOccurrencesByOrderUseCase  (tri par position, déjà ok ici)
types_and_positions = {("ABBAYE", 1): (0,0), ("ABBAYE", 2): (1,1)}
        │
        ▼ RemoveDuplicatesUseCase  (ABE et ABBAYE adjacents, même canonique)
label_preproc    = ["ABBAYE", "DES", "PINS"]
types_and_positions = {("ABBAYE", 1): (0,0)}
        │
        ▼ RemoveWrongDetectionsUseCase  (un seul type restant, rien à faire)
        │
        ▼ Résultat
InfoVoie.types_and_positions = {("ABBAYE", 1): (0, 0)}
```

---

## Ce qui n'est PAS fait dans `find_type`

| Responsabilité | Où c'est fait |
|---|---|
| Dilatation `ST→SAINT`, `DR→DOCTEUR`… | `SynonymsDilatationUseCase` (avant `find_type`) |
| Suppression de ponctuation | `PonctuationPreprocessorUseCase` (avant `find_type`) |
| Détection du complément (BATIMENT, RESIDENCE…) | `ComplementFinderUseCase` (après `find_type`) |
| Chargement du CSV de référence | `GenerateTypeFinderUtilsUseCase` (au démarrage) |
