import pandas as pd
from typing import Union

from decoupage_libelles.prepare_data.clean_type_voie.usecase.enrich_reduced_lib_use_case import EnrichReducedLibUseCase
from decoupage_libelles.prepare_data.clean_type_voie.usecase.choose_unique_lib_use_case import ChooseUniqueLibUseCase
from decoupage_libelles.prepare_data.clean_type_voie.usecase.new_codes_lib_use_case import NewCodesLibUseCase
from decoupage_libelles.prepare_data.clean_type_voie.usecase.create_dict_code_lib_use_case import CreatDictCodeLibUseCase
from decoupage_libelles.prepare_data.clean_type_voie.usecase.new_spelling_for_code_use_case import NewSpellingForCodeUseCase
from decoupage_libelles.config.settings_configuration import settings


class TypeVoieMajicPreprocessorUseCase:

    def __init__(
        self,
        enrich_reduced_lib_use_case: EnrichReducedLibUseCase = EnrichReducedLibUseCase(),
        choose_unique_lib_use_case: ChooseUniqueLibUseCase = ChooseUniqueLibUseCase(),
        new_codes_lib_use_case: NewCodesLibUseCase = NewCodesLibUseCase(),
        create_dict_code_lib_use_case: CreatDictCodeLibUseCase = CreatDictCodeLibUseCase(),
        new_spelling_for_code_use_case: NewSpellingForCodeUseCase = NewSpellingForCodeUseCase(),
    ):
        self.enrich_reduced_lib_use_case: EnrichReducedLibUseCase = enrich_reduced_lib_use_case
        self.choose_unique_lib_use_case: ChooseUniqueLibUseCase = choose_unique_lib_use_case
        self.new_codes_lib_use_case: NewCodesLibUseCase = new_codes_lib_use_case
        self.create_dict_code_lib_use_case: CreatDictCodeLibUseCase = create_dict_code_lib_use_case
        self.new_spelling_for_code_use_case: NewSpellingForCodeUseCase = new_spelling_for_code_use_case

    def execute(self) -> Union[pd.DataFrame, dict]:
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
        type_voie_df = pd.read_csv(settings.chemin_types_voies_majic)
        type_voie_df = self.enrich_reduced_lib_use_case.execute(type_voie_df)
        type_voie_df = self.choose_unique_lib_use_case.execute(type_voie_df)
        type_voie_df = self.new_codes_lib_use_case.execute(type_voie_df)
        code2lib = self.create_dict_code_lib_use_case.execute(type_voie_df)
        type_voie_df = self.new_spelling_for_code_use_case.execute(type_voie_df)

        return type_voie_df, code2lib
