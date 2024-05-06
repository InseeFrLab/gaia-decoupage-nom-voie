import pandas as pd
from typing import Union


class ChooseUniqueLibUseCase:
    UNIQUE_LIBS_FOR_CODES = ["CALLE", "DARSE", "SENTIER", "VALLEE"]
    OTHER_LIBS_FOR_CODES = ["CALLADA", "DARCE", "SENTE", "VALLON"]

    def execute(self, type_voie_df: pd.DataFrame) -> Union[pd.DataFrame, pd.DataFrame]:
        """
        Sélectionne un libellé unique pour les codes de type de voie qui en
        ont plusieurs.

        Cette méthode traite les cas où un même code de type de voie a
        plusieurs libellés associés, séparés par des barres '|'. Elle permet
        de choisir un libellé unique par code.

        La méthode extrait d'abord les libellés contenant des barres '|',
        les divise en libellés séparés,  puis réintègre une sélection de ces
        nouveaux libellés dans le DataFrame principal 'type_voie_df'.

        Retourne :
            DataFrame contenant les libellés et les codes.
        """
        list_barre = [elt for elt in type_voie_df["LIBELLE"].tolist() if "|" in elt]
        libs_for_code_df = type_voie_df[type_voie_df["LIBELLE"].isin(list_barre)]

        indices_a_supprimer = libs_for_code_df.index
        type_voie_df = type_voie_df.drop(indices_a_supprimer)

        libs_for_code_df = libs_for_code_df.assign(LIBELLE=libs_for_code_df["LIBELLE"].str.split("|")).explode("LIBELLE").reset_index(drop=True)

        unique_libs_for_codes_df = libs_for_code_df[libs_for_code_df["LIBELLE"].isin(ChooseUniqueLibUseCase.UNIQUE_LIBS_FOR_CODES)]
        other_libs_for_codes_df = pd.DataFrame({"CODE": ChooseUniqueLibUseCase.OTHER_LIBS_FOR_CODES, "LIBELLE": ChooseUniqueLibUseCase.OTHER_LIBS_FOR_CODES})
        type_voie_df = pd.concat([type_voie_df, unique_libs_for_codes_df], ignore_index=True)
        type_voie_df = pd.concat([type_voie_df, other_libs_for_codes_df], ignore_index=True)

        return type_voie_df
