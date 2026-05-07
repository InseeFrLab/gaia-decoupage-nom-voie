# Guide de contribution

Ce guide couvre les deux types de modifications les plus fréquentes :
1. Ajouter ou modifier des synonymes et variantes de types de voie.
2. Modifier les règles de détection dans les finders.

---

## 1. Ajouter des synonymes ou variantes de types de voie

### Cas A — ajouter une nouvelle variante pour un type existant

Exemple : on veut que `CHEM` soit reconnu comme variante de `CHEMIN`.

Ouvrir `src/decoupage_libelles/synonym_data/type_voie_synonyms.csv` et ajouter une ligne :

```csv
CHEMIN,CHEM,True,True,True
```

Format des colonnes :

| Colonne | Valeur | Description |
|---|---|---|
| `LIBELLE_CANONIQUE` | `CHEMIN` | La forme longue retournée en sortie — doit déjà exister dans le CSV |
| `VARIANTE` | `CHEM` | L'écriture à reconnaître dans les libellés |
| `MAJIC` | `True` / `False` | Cette variante apparaît dans le référentiel MAJIC |
| `BAN` | `True` / `False` | Cette variante apparaît dans la BAN |
| `RCA` | `True` / `False` | Cette variante apparaît dans le RCA |

> Si tu n'es pas sûr des colonnes MAJIC/BAN/RCA, mets `True` partout — c'est de l'information documentaire, pas fonctionnelle.

### Cas B — ajouter un type de voie entièrement nouveau

Exemple : ajouter `DRAILLE` comme type de voie (piste pastorale dans le Midi).

Ajouter **au minimum deux lignes** dans le CSV — la variante elle-même et le libellé canonique :

```csv
DRAILLE,DRAILLE,True,False,False
DRAILLE,DRA,True,False,False
```

La ligne `DRAILLE,DRAILLE` est obligatoire pour que le libellé complet soit détectable dans les adresses où le type est déjà écrit en toutes lettres.

> Attention : ajouter un nouveau type affecte les handlers. Si `DRAILLE` est un type longitudinal (comme `CHEMIN`), il faut aussi l'ajouter à `TYPESLONGITUDINAUX` et/ou `TYPESLONGITUDINAUX2` dans `type_is_longitudinal_or_agglomerant_use_case.py` (voir section 2).

### Cas C — ajouter une abréviation de mot courant (pas un type de voie)

Exemple : ajouter `CPTR` comme abréviation de `COMPTOIR`.

Ces abréviations ne sont pas des types de voie — elles concernent des mots qui apparaissent dans les noms de voie. Ouvrir `src/decoupage_libelles/synonym_data/extra_synonymes.csv` :

```csv
LIBELLE_CANONIQUE,VARIANTE
COMPTOIR,CPTR
```

La dilatation (`CPTR` → `COMPTOIR`) sera appliquée sur le `label_preproc` avant la détection de types.

### Tester les modifications

Après toute modification du CSV, vérifier que les tests passent :

```bash
python -m pytest tests/finders_tests/find_type_tests/ -v
```

Et tester manuellement sur quelques exemples réels :

```bash
# Depuis la racine du projet
python -c "
from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher
launcher = TypeVoieDecoupageLauncher()
res = launcher.execute(['DRAILLE DES MAURES', 'DRA DU BERGER'])
for r in res:
    print(r.label_origin, '->', r.type_assigned, '|', r.label_assigned)
"
```

---

## 2. Modifier les règles de détection dans les finders

### Modifier la liste des types longitudinaux ou agglomerants

Ces listes déterminent comment les handlers traitent les voies à 2 types.

**Fichier** : `src/decoupage_libelles/information_generators/type_in_lib/usecase/type_is_longitudinal_or_agglomerant_use_case.py`

```python
class TypeIsLongitudinalOrAgglomerantUseCase:

    # Utilisée quand il n'y a qu'1 type détecté
    TYPESLONGITUDINAUX = ["ROUTE", "BOULEVARD", "RUE", "AVENUE", "IMPASSE",
                          "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE"]

    # Utilisée quand il y a 2+ types détectés (inclut ALLEE)
    TYPESLONGITUDINAUX2 = ["ROUTE", "BOULEVARD", "RUE", "AVENUE", "IMPASSE",
                           "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE", "ALLEE"]

    TYPESAGGLOMERANTS = ["DOMAINE", "RESIDENCE", "HLM", "LOTISSEMENT", ...]
```

- **Longitudinal** = voie linéaire qu'on suit (rue, avenue, chemin…). Quand un type longitudinal est en première position, c'est généralement le vrai type de la voie.
- **Agglomerant** = zone ou groupement d'habitations (résidence, hameau, HLM…). Quand un type agglomerant est en première position, c'est souvent un complément d'adresse.

Pour ajouter `DRAILLE` comme type longitudinal :

```python
TYPESLONGITUDINAUX = [..., "DRAILLE"]
TYPESLONGITUDINAUX2 = [..., "DRAILLE"]
```

> Ajouter à `TYPESLONGITUDINAUX2` mais pas à `TYPESLONGITUDINAUX` créerait une asymétrie de comportement entre les voies à 1 type et les voies à 2 types. Toujours mettre à jour les deux sauf raison explicite.

### Modifier les types reconnus comme compléments

**Fichier** : `src/decoupage_libelles/finders/complement/usecase/complement_finder_use_case.py`

```python
class ComplementFinderUseCase:
    # Pour voies sans type détecté
    TYPES_COMPLEMENT_0 = ["PAVILLON", "IMMEUBLE", "BATIMENT", "BLOC",
                          "APPARTEMENT", "ESCALIER", "LOGEMENT", "ENTREE"]

    # Pour voies avec 1 ou 2 types détectés
    TYPES_COMPLEMENT_1_2 = ["PAVILLON", "IM", "IMMEUBLE", "BATIMENT", "BLOC",
                            "APPARTEMENT", "ESCALIER", "LOGEMENT", "ENTREE"]

    # Parmi les compléments : ceux qui indiquent un escalier ou appartement
    # (entraîne assign_lib au lieu de assign_type_lib)
    TYPES_APPART_ESC = ["BLOC", "APPARTEMENT", "ESCALIER"]
```

Pour ajouter `RESIDENCE` comme complément possible (dans les cas sans type détecté) :

```python
TYPES_COMPLEMENT_0 = [..., "RESIDENCE"]
```

> `RESIDENCE` est déjà dans `TYPESAGGLOMERANTS` — l'ajouter à `TYPES_COMPLEMENT_0` changerait le comportement pour les voies sans type : au lieu de passer par le handler no_type général, elles iraient dans `HandleNoTypeComplUseCase`.

### Modifier les types reconnus comme voies fictives

**Fichier** : `src/decoupage_libelles/finders/voie_fictive/usecase/voie_fictive_finder_use_case.py`

```python
class VoieFictiveFinderUseCase:
    # Lettres/chiffres qui indiquent une voie fictive (RUE A, IMPASSE 3…)
    LISTE_FICTIVE = ["A", "B", "C", ..., "1", "2", "3", ...]

    # Types concernés par la détection de voie fictive (1 type détecté)
    VOIES_FICTIVES_1 = ["BOULEVARD", "ALLEE", "RUE", "AVENUE", "IMPASSE",
                        "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE", "BATIMENT"]

    # Types concernés (2 types détectés) — inclut ROUTE en plus
    VOIES_FICTIVES_2 = ["ROUTE", ...] + VOIES_FICTIVES_1
```

Pour ajouter `DRAILLE` à la liste des types susceptibles d'avoir une voie fictive :

```python
VOIES_FICTIVES_1 = [..., "DRAILLE"]
VOIES_FICTIVES_2 = [..., "DRAILLE"]
```

### Modifier la table de priorité entre deux types longitudinaux

Quand deux types longitudinaux sont détectés (ex : `RUE HOCHE AVENUE VERDIER`), une table de 55 combinaisons détermine lequel prend la priorité.

**Fichier** : `src/decoupage_libelles/handlers/two_types/usecase/handle_has_type_in_first_pos_use_case.py`

```python
COMBINAISONS_LONG = {
    "RUE/ROUTE": True,   # True = le 1er type est prioritaire
    "ROUTE/RUE": False,  # False = le 2e type est prioritaire
    ...
}
```

Pour ajouter une règle pour `DRAILLE` :

```python
COMBINAISONS_LONG = {
    ...,
    "RUE/DRAILLE": True,   # RUE HOCHE DRAILLE DU BERGER → type=RUE, lib="HOCHE DRAILLE DU BERGER"
    "DRAILLE/RUE": False,  # DRAILLE DU BERGER RUE HOCHE → type=RUE, lib="DRAILLE DU BERGER HOCHE" ?
}
```

> Si la combinaison n'est pas dans le dict, le code tombe dans le cas par défaut (`type + lib` avec le 1er type). Un `logging.warning()` est émis pour signaler les combinaisons inconnues. Vérifier les logs après avoir ajouté un nouveau type longitudinal.

### Tester les modifications de règles

```bash
# Tests unitaires des handlers
python -m pytest tests/handlers_tests/ -v

# Tests des finders
python -m pytest tests/finders_tests/ -v

# Test de non-régression complet
python -m pytest tests/ -v
```
