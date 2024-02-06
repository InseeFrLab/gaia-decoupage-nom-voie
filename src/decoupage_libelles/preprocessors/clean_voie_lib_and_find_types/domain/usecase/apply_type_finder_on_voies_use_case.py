from injector import inject
from typing import List
import pandas as pd
from tqdm import tqdm

from finders.find_type.domain.usecase.type_finder_use_case import TypeFinderUseCase
from finders.find_type.domain.usecase.generate_type_finder_utils_use_case import GenerateTypeFinderUtilsUseCase
from voie_classes.voie import Voie
from finders.find_type.domain.model.type_finder_utils import TypeFinderUtils
from finders.find_type.domain.model.type_finder_object import TypeFinderObject


class ApplyTypeFinderOnVoiesUseCase:
    @inject
    def __init__(self, type_finder_use_case: TypeFinderUseCase, generate_type_finder_utils_use_case: GenerateTypeFinderUtilsUseCase):
        self.type_finder_use_case: TypeFinderUseCase = type_finder_use_case
        self.generate_type_finder_utils_use_case: GenerateTypeFinderUtilsUseCase = generate_type_finder_utils_use_case

    def execute(self, voies_data: List[Voie], type_voie_df: pd.DataFrame, code2lib: dict) -> List[Voie]:
        type_data = TypeFinderUtils(type_voie_df=type_voie_df, code2lib=code2lib)
        self.generate_type_finder_utils_use_case.execute(type_data)

        voies_data_detect_types = []
        for voie in tqdm(voies_data):
            voie_obj = TypeFinderObject(voie, type_data)
            new_voie = self.type_finder_use_case.execute(voie_obj)
            voies_data_detect_types.append(new_voie)

        return voies_data_detect_types