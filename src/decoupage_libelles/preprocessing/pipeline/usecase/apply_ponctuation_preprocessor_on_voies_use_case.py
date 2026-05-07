from typing import List

from decoupage_libelles.preprocessing.text_normalization.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie


class ApplyPonctuationPreprocessorOnVoiesUseCase:
    def __init__(
        self,
        ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = PonctuationPreprocessorUseCase(),
    ):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self, voies_data: List[InfoVoie]) -> List[InfoVoie]:
        voies_data_preprocessed_ponctuation = []
        for voie in voies_data:
            voie = self.ponctuation_preprocessor_use_case.execute(voie)
            voies_data_preprocessed_ponctuation.append(voie)

        return voies_data_preprocessed_ponctuation
