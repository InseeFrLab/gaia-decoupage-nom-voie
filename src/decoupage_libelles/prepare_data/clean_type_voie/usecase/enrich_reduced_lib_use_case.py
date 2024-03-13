import pandas as pd


class EnrichReducedLibUseCase:
    NEW_LIB_FOR_EXISTING_CODES = {
        "ZA": "ZONE D'ACTIVITES",
        "ZAC": "ZONE D'AMENAGEMENT CONCERTE",
        "ZAD": "ZONE D'AMENAGEMENT DIFFERE",
        "ZI": "ZONE INDUSTRIELLE",
        "ZUP": "ZONE A URBANISER EN PRIORITE",
    }

    def execute(self, type_voie_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrichit les codes qui ont aussi un code comme libellé dans
        le DataFrame.

        Cette méthode remplace les libellés existants dans la colonne 'LIBELLE'
        du DataFrame 'type_voie_df' par de nouveaux libellés spécifiés dans le
        dictionnaire 'new_lib_for_existing_codes'. Cela est utile pour
        remplacer les abréviations par des formes complètes.

        """
        type_voie_df["LIBELLE"] = type_voie_df["LIBELLE"].replace(EnrichReducedLibUseCase.NEW_LIB_FOR_EXISTING_CODES)
        return type_voie_df
