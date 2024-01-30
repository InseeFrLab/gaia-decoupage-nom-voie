import pandas as pd
from typing import List
from tqdm import tqdm

from voie_classes.voie import Voie
from preprocessors.ponctuation.domain.use_case.ponctuation_preprocessor_use_case import PonctuationPreprocessor
from constants.constant_lists import ponctuations
from finders.find_type.domain.usecase.generate_type_finder_utils_use_case import TypeFinderUtils
from finders.type_finder import TypeFinder


class VoieDataPreprocessor:
    def __init__(self,
                 voies_data: List[Voie],
                 type_voie_df: pd.DataFrame,
                 code2lib: dict):

        self.voies_data = voies_data
        self.type_voie_df = type_voie_df
        self.code2lib = code2lib

    def apply_ponctuation_preproc(self, ponctuations):
        voies_data_preproc_ponct = []
        for voie in tqdm(self.voies_data):
            voie = PonctuationPreprocessor().execute(voie, ponctuations)
            voies_data_preproc_ponct.append(voie)

        self.voies_data = voies_data_preproc_ponct

    def apply_detect_types(self):
        type_data = TypeFinderUtils(self.type_voie_df,
                                    self.code2lib)
        type_data.generate_type_detector_utils()

        voies_data_detect_types = []
        for voie in tqdm(self.voies_data):
            voie = TypeFinder(voie, type_data).run()
            voies_data_detect_types.append(voie)

        self.voies_data = voies_data_detect_types

    def run(self):
        print("Traitement de la ponctuation")
        self.apply_ponctuation_preproc(ponctuations)
        print("Détection des types de voies dans les libellés")
        self.apply_detect_types()
        return self.voies_data
