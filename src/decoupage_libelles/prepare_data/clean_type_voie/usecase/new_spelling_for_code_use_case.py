import pandas as pd

from decoupage_libelles.prepare_data.clean_type_voie.usecase.apply_ponctuation_preprocessing_on_type_voie_use_case import ApplyPonctuationPreprocessingOnTypeVoie


class NewSpellingForCodeUseCase:
    OTHER_LIBS_FOR_CODES = ["CALLADA", "DARCE", "SENTE", "VALLON"]

    OTHER_SPELLING_FOR_CODES = [
        {"CODE": "CHP", "LIBELLE": "CHAMPS"},
        {"CODE": "GR", "LIBELLE": "GDE RUE"},
        {"CODE": "ACH", "LIBELLE": "ANCIEN CHEM"},
        {"CODE": "ACH", "LIBELLE": "ANC CHEM"},
        {"CODE": "ART", "LIBELLE": "ANC RTE"},
        {"CODE": "ACH", "LIBELLE": "ANC CHEMIN"},
        {"CODE": "VCHE", "LIBELLE": "VX CHEMIN"},
        {"CODE": "VCHE", "LIBELLE": "VX CHE"},
        {"CODE": "VCHE", "LIBELLE": "VX CHEM"},
        {"CODE": "ART", "LIBELLE": "ANC ROUTE"},
        {"CODE": "PCH", "LIBELLE": "PT CHEM"},
        {"CODE": "ZAE", "LIBELLE": "ZONE D'ACTIVITES ECONOMIQUES"},
        {"CODE": "ZA", "LIBELLE": "PARC D'ACTIVITES"},
        {"CODE": "AV", "LIBELLE": "AVE"},
        {"CODE": "PTR", "LIBELLE": "PTE RUE"},
        {"CODE": "VGE", "LIBELLE": "VILLAG"},
        {"CODE": "GRA", "LIBELLE": "GDE ALLEE"},
        {"CODE": "APL", "LIBELLE": "ANC PL"},
        {"CODE": "ANV", "LIBELLE": "ANC VOIE"},
        {"CODE": "GPL", "LIBELLE": "GDE PCE"},
        {"CODE": "GR", "LIBELLE": "GR RUE"},
        {"CODE": "GAV", "LIBELLE": "GDE AV"},
        {"CODE": "QUA", "LIBELLE": "QU"},
    ]

    def __init__(
        self,
        apply_ponctuation_preprocessing_on_type_voie_use_case: ApplyPonctuationPreprocessingOnTypeVoie = ApplyPonctuationPreprocessingOnTypeVoie(),
    ):
        self.apply_ponctuation_preprocessing_on_type_voie_use_case: ApplyPonctuationPreprocessingOnTypeVoie = apply_ponctuation_preprocessing_on_type_voie_use_case

    def execute(self, type_voie_df: pd.DataFrame, libs_for_code_df: pd.DataFrame) -> pd.DataFrame:
        """
        Ajoute de nouvelles orthographes pour les codes de types de voie.

        Cette méthode enrichit le DataFrame 'type_voie_df' avec des
        orthographes alternatives pour les libellés de types de voie.
        Elle prend un DataFrame 'libs_for_code_df' contenant des libellés
        alternatifs et les intègre dans le DataFrame principal. Ensuite,
        elle ajoute d'autres orthographes spécifiées dans
        'other_spelling_for_codes'.

        Les nouvelles entrées sont triées par code et l'index du DataFrame est
        réinitialisé pour garantir la cohérence.

        Paramètres :
        - libs_for_code_df : DataFrame contenant les libellés alternatifs
                            à ajouter.
        """
        other_libs_for_codes_df = libs_for_code_df[libs_for_code_df["LIBELLE"].isin(NewSpellingForCodeUseCase.OTHER_LIBS_FOR_CODES)]
        type_voie_df = pd.concat([type_voie_df, other_libs_for_codes_df], ignore_index=True)
        new_row_df = pd.DataFrame(NewSpellingForCodeUseCase.OTHER_SPELLING_FOR_CODES)

        type_voie_df = pd.concat([type_voie_df, new_row_df], ignore_index=True).sort_values(by="CODE", ascending=True).reset_index(drop=True)
        type_voie_df["LIBELLE"] = type_voie_df["LIBELLE"].apply(self.apply_ponctuation_preprocessing_on_type_voie_use_case.execute)

        return type_voie_df
