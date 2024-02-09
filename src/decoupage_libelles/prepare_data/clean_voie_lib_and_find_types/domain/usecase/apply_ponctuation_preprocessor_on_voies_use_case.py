from injector import inject
from typing import List
from tqdm import tqdm

from prepare_data.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from informations_on_libelle_voie.model.infovoie import InfoVoie


class ApplyPonctuationPreprocessorOnVoiesUseCase:
    def __init__(self, ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self, voies_data: List[InfoVoie]) -> List[InfoVoie]:
            voies_data_preprocessed_ponctuation = []
            for voie in tqdm(voies_data):
                voie = self.ponctuation_preprocessor_use_case.execute(voie)
                voies_data_preprocessed_ponctuation.append(voie)

            return voies_data_preprocessed_ponctuation