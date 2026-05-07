# Architecture du code

## Structure des dossiers

```
gaia-decoupage-libelles-voies/
├── config.yml                              ← configuration utilisateur (plateforme, fichiers, colonnes)
├── src/
│   └── decoupage_libelles/
│       ├── config/                         ← pipeline principale + settings applicatifs
│       ├── entrypoints/                    ← points d'entrée (API web, traitement batch)
│       │   ├── web/
│       │   └── batch/
│       ├── handlers/                       ← arbre de décision par nombre de types détectés
│       │   ├── no_type/
│       │   ├── one_type/
│       │   ├── two_types/
│       │   └── two_types_and_more/
│       ├── preprocessing/                  ← préparation des libellés avant détection
│       │   ├── text_normalization/         ← suppression ponctuation, dilatation synonymes
│       │   └── pipeline/                   ← orchestration du prétraitement complet
│       ├── information_generators/         ← calcul des propriétés d'une voie ou d'un type
│       │   ├── libelle/                    ← infos sur le libellé global (positions, postag…)
│       │   └── type_in_lib/               ← infos sur un type précis (longitudinal, complément…)
│       ├── finders/                        ← détection des éléments dans le libellé
│       │   ├── type/                       ← détection du type de voie (RUE, AVENUE, CHE…)
│       │   ├── complement/                 ← détection du complément (BAT, PAVILLON…)
│       │   └── voie_fictive/              ← détection des voies fictives (RUE A, AVENUE B…)
│       ├── decoupage_final_constructors/  ← construction du résultat final (assign_*)
│       └── synonym_data/                  ← données de référence (CSV types de voie, synonymes)
└── tests/
    ├── finders_tests/
    ├── handlers_tests/
    └── entrypoints_tests/
```

---

## Rôle de chaque module

### `config/`
Contient deux fichiers :
- `settings_configuration.py` — chemins des modèles NLP et données de référence, chargés via Dynaconf.
- `type_voie_decoupage_launcher.py` — orchestrateur principal : crée les `InfoVoie`, appelle le prétraitement, route vers le bon handler selon le nombre de types détectés.

### `entrypoints/`
Points d'entrée de l'application. Ne contiennent pas de logique métier.
- `web/main_api.py` — API FastAPI exposant `/analyse-libelles-voies`.
- `batch/run.py` — script de traitement batch, lit `config.yml` et orchestre la parallélisation.
- `batch/parallel_processor.py` — `ThreadPoolExecutor`, découpage en chunks, appel à l'API.
- `batch/storage.py` — lecture/écriture fichiers CSV, parquet, dossier parquet, en local et sur S3.
- `batch/data_preparation.py` — construction de la colonne de libellé et post-traitement MAJIC.

### `preprocessing/`
Prépare les libellés bruts avant la détection de types.
- `text_normalization/` — mise en majuscules, suppression de ponctuation, séparation sur apostrophe, dilatation des synonymes extra (`ST` → `SAINT`, `DR` → `DOCTEUR`…). Ces transformations sont appliquées **aussi bien sur les libellés d'adresse que sur les variantes du CSV de référence**, pour que la comparaison se fasse dans le même espace.
- `pipeline/` — `VoieLibPreprocessorUseCase` qui enchaîne le prétraitement de ponctuation puis la détection de types sur toutes les voies.

### `information_generators/`
Calcule les propriétés nécessaires à l'arbre de décision des handlers.
- `libelle/` — analyse du libellé global : positions des types (1ère, 2e, dernière position), postag NLP, liste des types détectés, doublons.
- `type_in_lib/` — analyse d'un type précis dans son contexte : est-il longitudinal (RUE, AVENUE…) ? agglomerant (RESIDENCE, HLM…) ? complément (BAT, PAVILLON…) ? Quel mot le précède et le suit ?

### `finders/`
Détecte des éléments dans le libellé prétraité.
- `type/` — détecte les types de voie en cherchant toutes les variantes connues (mono et multi-mots) dans `label_preproc`. Nettoie les faux positifs (type court inclus dans un type long).
- `complement/` — détecte le premier type "complément" (`BATIMENT`, `PAVILLON`…) dans le libellé.
- `voie_fictive/` — détecte si le type est suivi d'une lettre ou d'un chiffre isolé (`RUE A`, `IMPASSE 3`…), indiquant une voie nommée par lettre plutôt qu'un vrai libellé.

### `handlers/`
Arbre de décision principal. Chaque handler reçoit une liste de voies filtrées selon le nombre de types détectés, cherche d'abord un complément, puis une voie fictive, puis traite le reste selon la position des types.

Voir [code/detection_type_voie.md](code/detection_type_voie.md) pour le détail de la détection de type, et [code/handlers/overview.md](code/handlers/overview.md) pour l'arbre de décision complet des handlers.

### `decoupage_final_constructors/`
Une fois l'arbre de décision parcouru, l'un des 8 use cases `assign_*` construit le `VoieDecoupee` final en délimitant ce qui est `type_assigned`, `label_assigned` et `compl_assigned`.

| Use case | Pattern |
|---|---|
| `assign_lib` | tout en libellé |
| `assign_type_lib` | type + libellé |
| `assign_lib_type` | libellé + type |
| `assign_lib_compl` | libellé + complément |
| `assign_type_lib_compl` | type + libellé + complément |
| `assign_compl_type_lib` | complément + type + libellé |
| `assign_compl_type_lib_compl` | complément + type + libellé + complément |
| `assign_type` | type seul |

### `synonym_data/`
Fichiers CSV de référence chargés au démarrage :
- `type_voie_synonyms.csv` — toutes les variantes connues pour chaque type de voie canonique.
- `extra_synonymes.csv` — abréviations courantes dans les adresses (`ST`, `DR`, `LT`…).

---

## Flux de données

```
libellé brut ("RUE HOCHE" / "CHE DES SEMAPHORES" / "HLM AV KLEBER BAT B")
        │
        ▼ preprocessing/text_normalization
label_preproc = ["RUE", "HOCHE"]    ← ponctuation nettoyée, synonymes dilatés
        │
        ▼ finders/type
types_and_positions = {("RUE", 1): (0, 0)}
        │
        ▼ TypeVoieDecoupageLauncher — routage selon len(types_and_positions)
        │
        ├── 0 type  → handlers/no_type
        ├── 1 type  → handlers/one_type
        └── 2+ types → handlers/two_types_and_more
                            │
                            ▼ filtrage NLP (KeepTypesWithoutArticleAdjBefore)
                            ├── 0 → assign_lib
                            ├── 1 → handlers/one_type
                            └── 2 → handlers/two_types
        │
        ▼ decoupage_final_constructors/assign_*
VoieDecoupee(type="RUE", label="HOCHE", compl="")
```
