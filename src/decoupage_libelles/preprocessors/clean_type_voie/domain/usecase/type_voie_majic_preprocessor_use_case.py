import pandas as pd
from injector import inject

from preprocessors.clean_type_voie.domain.usecase.enrich_reduced_lib_use_case import EnrichReducedLibUseCase
from preprocessors.clean_type_voie.domain.usecase.choose_unique_lib_use_case import ChooseUniqueLibUseCase
from preprocessors.clean_type_voie.domain.usecase.new_codes_lib_use_case import NewCodesLibUseCase
from preprocessors.clean_type_voie.domain.usecase.create_dict_code_lib_use_case import CreatDictCodeLibUseCase
from preprocessors.clean_type_voie.domain.usecase.new_spelling_for_code_use_case import NewSpellingForCodeUseCase


class TypeVoieMajicPreprocessorUseCase:
    FILEPATH_TYPE_VOIE = "../data/type_voie_majic.csv"

    def __init__(self, enrich_reduced_lib_use_case: EnrichReducedLibUseCase, choose_unique_lib_use_case: ChooseUniqueLibUseCase,
                 new_codes_lib_use_case: NewCodesLibUseCase, create_dict_code_lib_use_case: CreatDictCodeLibUseCase, new_spelling_for_code_use_case: NewSpellingForCodeUseCase):
        self.enrich_reduced_lib_use_case: EnrichReducedLibUseCase = enrich_reduced_lib_use_case
        self.choose_unique_lib_use_case: ChooseUniqueLibUseCase = choose_unique_lib_use_case
        self.new_codes_lib_use_case: NewCodesLibUseCase = new_codes_lib_use_case
        self.create_dict_code_lib_use_case: CreatDictCodeLibUseCase = create_dict_code_lib_use_case
        self.new_spelling_for_code_use_case: NewSpellingForCodeUseCase = new_spelling_for_code_use_case

    def execute(self) -> (pd.DataFrame, dict):
        """
        Nettoie et enrichit les données de type de voie.

        Cette méthode exécute une série d'opérations de nettoyage et
        d'enrichissement sur le DataFrame 'type_voie_df', qui contient
        les codes et libellés des types de voie. Elle commence par
        sélectionner un libellé unique pour chaque code,
        ajoute de nouveaux codes non présents dans les données initiales,
        crée un dictionnaire mappant les codes aux libellés,
        et ajoute différentes orthographes pour les codes.

        Retourne : Le DataFrame nettoyé et un dictionnaire des codes
        avec libellés uniques.
        """
        type_voie_df = pd.read_csv(TypeVoieMajicPreprocessorUseCase.FILEPATH_TYPE_VOIE)
        self.enrich_reduced_lib_use_case.execute(type_voie_df)
        libs_for_code_df = self.choose_unique_lib_use_case.execute(type_voie_df)
        self.new_codes_lib_use_case.execute(type_voie_df)
        code2lib = self.create_dict_code_lib_use_case.execute(type_voie_df)
        self.new_spelling_for_code_use_case.execute(type_voie_df, libs_for_code_df)

        return type_voie_df, code2lib
