from typing import List


class SeparatePonctuationAndWordsWithApostrophe:
    def execute(self, label_raw: str, ponctuations: List[str]) -> List[str]:
        voie = label_raw
        # séparer le libellé en liste de mots
        new_voie = voie.split(" ")
        # séparer en deux les mots avec apostrophe
        new_voie = [mot.split("'") for mot in new_voie]
        new_voie = [mot for item in new_voie for mot in item]
        new_voie = [segment for mot in new_voie for segment in re.split(r"(\d+)", mot) if segment]
        # retirer les ponctuations seules et les espaces en trop
        self.new_voie_traitee = [item for item in new_voie if (item not in self.ponctuations and item != "")]
