import pandas as pd


class NewCodesLibUseCase:
    NEW_CODES = [{'CODE': 'ZAE',
                 'LIBELLE': "ZONE D'ACTIVITES ECONOMIQUES"},
                 {'CODE': 'GRA',
                 'LIBELLE': "GRANDE ALLEE"},
                 {'CODE': 'APL',
                 'LIBELLE': "ANCIENNE PLACE"},
                 {'CODE': 'ANV',
                 'LIBELLE': "ANCIENNE VOIE"},]

    def execute(self, type_voie_df: pd.DataFrame) -> pd.DataFrame:
        """
        Ajoute un nouveau code de type de voie au DataFrame.

        Cette méthode crée une nouvelle ligne dans le DataFrame 'type_voie_df'
        pour un code de type de voie qui n'était pas présent dans les données
        originales. Le nouveau code et son libellé correspondant sont définis
        dans le dictionnaire 'new_codes'.

        Après l'ajout, le DataFrame est trié par le code de type de voie pour
        maintenir l'ordre, et l'index est réinitialisé pour une meilleure
        cohérence.
        """
        new_row_df = pd.DataFrame(NewCodesLibUseCase.NEW_CODES)
        type_voie_df = pd.concat([type_voie_df, new_row_df],
                                      ignore_index=True
                                      ).sort_values(by='CODE'
                                                    ).reset_index(drop=True)
        return type_voie_df