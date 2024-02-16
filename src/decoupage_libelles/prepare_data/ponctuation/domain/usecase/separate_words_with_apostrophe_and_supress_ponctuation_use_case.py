from typing import List
import re


class SeparateWordsWithApostropheAndSupressPonctuationUseCase:
    def execute(self, label_raw: str, ponctuations: List[str]) -> List[str]:
        voie = label_raw
        # séparer le libellé en liste de mots
        voie_separated = voie.split(" ")
        # séparer en deux les mots avec apostrophe
        voie_separated_apostrophe = [mot.split("'") for mot in voie_separated]
        voie_separated_without_apostrophe = [mot for item in voie_separated_apostrophe for mot in item]
        voie_separated_without_apostrophe = [segment for mot in voie_separated_without_apostrophe for segment in re.split(r"(\d+)", mot) if segment]
        # retirer les ponctuations seules et les espaces en trop
        voie_treated = [item for item in voie_separated_without_apostrophe if (item not in ponctuations and item != "")]
        return voie_treated
