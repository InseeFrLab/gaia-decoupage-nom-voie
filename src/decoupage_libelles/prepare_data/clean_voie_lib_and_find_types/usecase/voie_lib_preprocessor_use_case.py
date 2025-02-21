import pandas as pd
from typing import List
import logging

from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.apply_ponctuation_preprocessor_on_voies_use_case import ApplyPonctuationPreprocessorOnVoiesUseCase
from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.apply_type_finder_on_voies_use_case import ApplyTypeFinderOnVoiesUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class VoieLibPreprocessorUseCase:
    def __init__(
        self,
        apply_ponctuation_preprocessor_on_voies_use_case: ApplyPonctuationPreprocessorOnVoiesUseCase = ApplyPonctuationPreprocessorOnVoiesUseCase(),
        apply_type_finder_on_voies_use_case: ApplyTypeFinderOnVoiesUseCase = ApplyTypeFinderOnVoiesUseCase(),
    ):
        self.apply_ponctuation_preprocessor_on_voies_use_case: ApplyPonctuationPreprocessorOnVoiesUseCase = apply_ponctuation_preprocessor_on_voies_use_case
        self.apply_type_finder_on_voies_use_case: ApplyTypeFinderOnVoiesUseCase = apply_type_finder_on_voies_use_case

    def execute(self, voies_data: List[InfoVoie], type_voie_df: pd.DataFrame, code2lib: dict) -> List[InfoVoie]:
        logging.info("Traitement de la ponctuation")
        self.apply_ponctuation_preprocessor_on_voies_use_case.execute(voies_data)
        logging.info("Détection des types de voies dans les libellés")
        self.apply_type_finder_on_voies_use_case.execute(voies_data, type_voie_df, code2lib)
        return voies_data
