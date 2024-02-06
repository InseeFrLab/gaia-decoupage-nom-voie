from injector import inject
from typing import List
from tqdm import tqdm

from preprocessors.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from voie_classes.voie import Voie


class ApplyPonctuationPreprocessorOnVoiesUseCase:
    def __init__(self, ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self, voies_data: List[Voie]) -> List[Voie]:
            voies_data_preprocessed_ponctuation = []
            for voie in tqdm(voies_data):
                voie = self.ponctuation_preprocessor_use_case.execute(voie)
                voies_data_preprocessed_ponctuation.append(voie)

            return voies_data_preprocessed_ponctuation