import pandas as pd

from decoupage_libelles.prepare_data.clean_type_voie.usecase.apply_ponctuation_preprocessing_on_type_voie_use_case import ApplyPonctuationPreprocessingOnTypeVoie


class NewSpellingForCodeUseCase:
    OTHER_SPELLING_FOR_CODES = [
        {"CODE": "VOIE", "LIBELLE": "VOI"},
        {"CODE": "PTR", "LIBELLE": "PR"},
        {"CODE": "CHP", "LIBELLE": "CHAMPS"},
        {"CODE": "CHP", "LIBELLE": "CHPS"},
        {"CODE": "AV", "LIBELLE": "AVE"},
        {"CODE": "PTR", "LIBELLE": "PTE RUE"},
        {"CODE": "VGE", "LIBELLE": "VILLAG"},
        {"CODE": "VGE", "LIBELLE": "VLG"},
        {"CODE": "QUAI", "LIBELLE": "QU"},
        {"CODE": "ILOT", "LIBELLE": "ILO"},
        {"CODE": "QUA", "LIBELLE": "QRT"},
        {"CODE": "RD", "LIBELLE": "DEPARTEMENTALE"},
        # {"CODE": "RD", "LIBELLE": "RTE D"},
        # {"CODE": "RD", "LIBELLE": "ROUTE D"},
        {"CODE": "FG", "LIBELLE": "FBG"},
        {"CODE": "LD", "LIBELLE": "LDT"},
        {"CODE": "LD", "LIBELLE": "LIEUDIT"},
        {"CODE": "VGE", "LIBELLE": "VLGE"},
        {"CODE": "CCAL", "LIBELLE": "CCIAL"},
        # {"CODE": "IMM", "LIBELLE": "IM"},
        {"CODE": "RN", "LIBELLE": "NATIONALE"},
        # {"CODE": "RN", "LIBELLE": "RTE N"},
        # {"CODE": "RN", "LIBELLE": "ROUTE N"},
        {"CODE": "CLOS", "LIBELLE": "CLS"},
        {"CODE": "MLN", "LIBELLE": "MOUL"},
    ]

    def __init__(
        self,
        apply_ponctuation_preprocessing_on_type_voie_use_case: ApplyPonctuationPreprocessingOnTypeVoie = ApplyPonctuationPreprocessingOnTypeVoie(),
    ):
        self.apply_ponctuation_preprocessing_on_type_voie_use_case: ApplyPonctuationPreprocessingOnTypeVoie = apply_ponctuation_preprocessing_on_type_voie_use_case

    def execute(self, type_voie_df: pd.DataFrame) -> pd.DataFrame:
        """
        Ajoute de nouvelles orthographes pour les codes de types de voie.

        Cette méthode enrichit le DataFrame 'type_voie_df' avec des
        orthographes alternatives pour les libellés de types de voie.
        Elle ajoute d'autres orthographes spécifiées dans
        'other_spelling_for_codes'.

        Les nouvelles entrées sont triées par code et l'index du DataFrame est
        réinitialisé pour garantir la cohérence.
        """

        new_row_df = pd.DataFrame(NewSpellingForCodeUseCase.OTHER_SPELLING_FOR_CODES)

        type_voie_df = pd.concat([type_voie_df, new_row_df], ignore_index=True).sort_values(by="CODE", ascending=True).reset_index(drop=True)
        type_voie_df["LIBELLE"] = type_voie_df["LIBELLE"].apply(self.apply_ponctuation_preprocessing_on_type_voie_use_case.execute)

        return type_voie_df
