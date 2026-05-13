from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
import re
import pandas as pd
from decoupage_libelles.config.settings_configuration import settings


class DilatedVoieDecoupeeUseCase:
    type_voie_df: pd.DataFrame = pd.read_csv(settings.chemin_type_voie)

    DILATATION_TYPE_VOIE = dict(
        zip(type_voie_df["VARIANTE"], type_voie_df["LIBELLE_CANONIQUE"])
    )

    synonyms_extra_df: pd.DataFrame = pd.read_csv(settings.chemin_synonymes_extra)

    DILATATION_NOM_VOIE = dict(
        zip(synonyms_extra_df["VARIANTE"], synonyms_extra_df["LIBELLE_CANONIQUE"])
    )

    DILATATION_COMPLEMENT = DILATATION_TYPE_VOIE | DILATATION_NOM_VOIE

    def execute(self, voiedecoupee: VoieDecoupee) -> VoieDecoupee:
        for acronym, full_form in DilatedVoieDecoupeeUseCase.DILATATION_TYPE_VOIE.items():
            voiedecoupee.type_assigned = re.sub(rf'\b{acronym}\b', full_form, voiedecoupee.type_assigned, flags=re.IGNORECASE).lower()
        for acronym, full_form in DilatedVoieDecoupeeUseCase.DILATATION_NOM_VOIE.items():
            voiedecoupee.label_assigned = re.sub(rf'\b{acronym}\b', full_form, voiedecoupee.label_assigned, flags=re.IGNORECASE).lower()
        for acronym, full_form in DilatedVoieDecoupeeUseCase.DILATATION_COMPLEMENT.items():
            voiedecoupee.compl_assigned = re.sub(rf'\b{acronym}\b', full_form, voiedecoupee.compl_assigned, flags=re.IGNORECASE).lower()

        voiedecoupee.compl2 = voiedecoupee.compl2.lower()
        return voiedecoupee
