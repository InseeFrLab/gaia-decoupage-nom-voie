from typing import List
import pandas as pd

from decoupage_libelles.finders.find_type.usecase.type_finder_use_case import TypeFinderUseCase
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import GenerateTypeFinderUtilsUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class ApplyTypeFinderOnVoiesUseCase:
    def __init__(
        self,
        type_finder_use_case: TypeFinderUseCase = TypeFinderUseCase(),
        generate_type_finder_utils_use_case: GenerateTypeFinderUtilsUseCase = GenerateTypeFinderUtilsUseCase(),
    ):
        self.type_finder_use_case: TypeFinderUseCase = type_finder_use_case
        self.generate_type_finder_utils_use_case: GenerateTypeFinderUtilsUseCase = generate_type_finder_utils_use_case

    def execute(self, voies_data: List[InfoVoie], type_voie_df: pd.DataFrame, code2lib: dict) -> List[InfoVoie]:
        type_data = TypeFinderUtils(type_voie_df=type_voie_df, code2lib=code2lib)
        self.generate_type_finder_utils_use_case.execute(type_data)

        voies_data_detect_types = []
        for voie in voies_data:
            voie_obj = TypeFinderObject(voie, type_data)
            new_voie = self.type_finder_use_case.execute(voie_obj)
            voies_data_detect_types.append(new_voie)

        return voies_data_detect_types
