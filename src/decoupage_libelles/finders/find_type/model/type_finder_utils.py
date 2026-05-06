from dataclasses import dataclass, field
from typing import Dict, List, Set
import pandas as pd
from decoupage_libelles.config.settings_configuration import settings


@dataclass
class TypeFinderUtils:
    """
    Contient les données de référence pour la détection de types de voie.

    type_voie_df : DataFrame avec colonnes ['LIBELLE_CANONIQUE', 'VARIANTE']
                   Chaque ligne associe une variante (écriture possible) à son
                   libellé canonique (forme longue de référence).
                   Ex : LIBELLE_CANONIQUE='AVENUE', VARIANTE='AV'
                        LIBELLE_CANONIQUE='AVENUE', VARIANTE='AVE'

    variante2canonique : dict {variante -> libellé_canonique}
    canoniques         : ensemble des libellés canoniques uniques
    variantes_multi    : variantes composées de plusieurs mots (ex: 'ANCIEN CHEMIN')
    variantes_mono     : variantes d'un seul mot (ex: 'AV', 'AVENUE', 'CHE')
    variante2preproc   : dict {variante_raw -> variante_prétraitée}
    """
    type_voie_df: pd.DataFrame = field(
        default_factory=lambda: pd.read_csv(settings.chemin_type_voie)
    )
    variante2canonique: Dict[str, str] = field(default_factory=dict)
    canoniques: Set[str] = field(default_factory=set)
    variantes_multi: List[str] = field(default_factory=list)
    variantes_mono: List[str] = field(default_factory=list)
    variante2preproc: Dict[str, str] = field(default_factory=dict)
