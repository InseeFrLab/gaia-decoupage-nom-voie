import re
from typing import List
import pandas as pd
from decoupage_libelles.config.settings_configuration import settings


class SynonymsDilatationUseCase:
    @classmethod
    def _load_extra_synonyms(cls) -> dict:
        df = pd.read_csv(settings.chemin_synonymes_extra)
        # VARIANTE → LIBELLE_CANONIQUE  (même convention que le reste du projet)
        return dict(zip(df["VARIANTE"], df["LIBELLE_CANONIQUE"]))

    EXTRA_SYNONYMS: dict = None  # chargé en lazy au premier appel

    def execute(self, label_preproc: List[str]) -> List[str]:
        label_preproc = (' ').join(label_preproc)

        for acronym, full_form in SynonymsDilatationUseCase.EXTRA_SYNONYMS.items():
            label_preproc = re.sub(rf'\b{acronym}\b', full_form, label_preproc, flags=re.IGNORECASE)

        label_preproc_dilated = label_preproc.split(' ')

        return label_preproc_dilated
