import pandas as pd
from typing import List
import logging

from decoupage_libelles.preprocessing.pipeline.usecase.apply_ponctuation_preprocessor_on_voies_use_case import ApplyPonctuationPreprocessorOnVoiesUseCase
from decoupage_libelles.preprocessing.pipeline.usecase.apply_type_finder_on_voies_use_case import ApplyTypeFinderOnVoiesUseCase
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie


class VoieLibPreprocessorUseCase:
    def __init__(
        self,
        apply_ponctuation_preprocessor_on_voies_use_case: ApplyPonctuationPreprocessorOnVoiesUseCase = ApplyPonctuationPreprocessorOnVoiesUseCase(),
        apply_type_finder_on_voies_use_case: ApplyTypeFinderOnVoiesUseCase = ApplyTypeFinderOnVoiesUseCase(),
    ):
        self.apply_ponctuation_preprocessor_on_voies_use_case: ApplyPonctuationPreprocessorOnVoiesUseCase = apply_ponctuation_preprocessor_on_voies_use_case
        self.apply_type_finder_on_voies_use_case: ApplyTypeFinderOnVoiesUseCase = apply_type_finder_on_voies_use_case

    def execute(self, voies_data: List[InfoVoie]) -> List[InfoVoie]:
        logging.info("Traitement de la ponctuation")
        self.apply_ponctuation_preprocessor_on_voies_use_case.execute(voies_data)
        logging.info("Détection des types de voies dans les libellés")
        self.apply_type_finder_on_voies_use_case.execute(voies_data)
        return voies_data
