import pandas as pd
from injector import inject
from typing import List

from preprocessors.clean_voie_lib_and_find_types.domain.usecase.apply_ponctuation_preprocessor_on_voies_use_case import ApplyPonctuationPreprocessorOnVoiesUseCase
from preprocessors.clean_voie_lib_and_find_types.domain.usecase.apply_type_finder_on_voies_use_case import ApplyTypeFinderOnVoiesUseCase
from voie_classes.voie import Voie


class VoieLibPreprocessorUseCase:
    @inject
    def __init__(self, apply_ponctuation_preprocessor_on_voies_use_case: ApplyPonctuationPreprocessorOnVoiesUseCase,
                 apply_type_finder_on_voies_use_case: ApplyTypeFinderOnVoiesUseCase):
        self.apply_ponctuation_preprocessor_on_voies_use_case: ApplyPonctuationPreprocessorOnVoiesUseCase = apply_ponctuation_preprocessor_on_voies_use_case
        self.apply_type_finder_on_voies_use_case: ApplyTypeFinderOnVoiesUseCase = apply_type_finder_on_voies_use_case

    def run(self, voies_data: List[Voie], type_voie_df: pd.DataFrame, code2lib: dict) -> List[Voie]:
        print("Traitement de la ponctuation")
        self.apply_ponctuation_preprocessor_on_voies_use_case.execute(voies_data)
        print("Détection des types de voies dans les libellés")
        self.apply_type_finder_on_voies_use_case.execute(voies_data, type_voie_df, code2lib)
        return voies_data
