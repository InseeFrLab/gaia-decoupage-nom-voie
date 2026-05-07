import re
from typing import List
import pandas as pd
from decoupage_libelles.config.settings_configuration import settings


class SynonymsDilatationUseCase:
    EXTRA_SYNONYMS: dict = None

    @classmethod
    def _load_extra_synonyms(cls) -> dict:
        df = pd.read_csv(settings.chemin_synonymes_extra)

        # VARIANTE → LIBELLE_CANONIQUE
        return dict(zip(df["VARIANTE"], df["LIBELLE_CANONIQUE"]))

    def execute(self, label_preproc: List[str]) -> List[str]:

        # Lazy loading
        if SynonymsDilatationUseCase.EXTRA_SYNONYMS is None:
            SynonymsDilatationUseCase.EXTRA_SYNONYMS = (
                SynonymsDilatationUseCase._load_extra_synonyms()
            )

        label_preproc = ' '.join(label_preproc)

        for acronym, full_form in SynonymsDilatationUseCase.EXTRA_SYNONYMS.items():
            label_preproc = re.sub(
                rf'\b{re.escape(acronym)}\b',
                full_form,
                label_preproc,
                flags=re.IGNORECASE,
            )

        return label_preproc.split(' ')
