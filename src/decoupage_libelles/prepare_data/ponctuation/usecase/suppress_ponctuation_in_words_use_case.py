from typing import List
import re


class SuppressPonctuationInWordsUseCase:
    def execute(self, chaine_traitee: List[str], ponctuations: List[str]) -> List[str]:
        # retirer la ponctuation contenue dans un mot
        new_label_preproc = []
        for mot in chaine_traitee:
            mot_sep = re.split(r"([-_.,;:!?\[\]\(\){}*\/°«»\"\\])", mot)
            mot_sep = [ss for ss in mot_sep if ss.strip()]
            new_mot = [ss for ss in mot_sep if ss not in ponctuations]
            for sous_mot in new_mot:
                new_label_preproc.append(sous_mot)
        return new_label_preproc
