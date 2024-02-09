from typing import List
import re


class SuppressPonctuationInWordsUseCase:
    def execute(self, chaine_traitee: List[str], ponctuations: List[str]) -> List[str]:
        # retirer la ponctuation contenue dans un mot
        new_label_preproc = chaine_traitee[:]
        for j, mot in enumerate(chaine_traitee):
            mot_sep = re.split(r"([-.,;:!?(){}*/])", mot)
            mot_sep = [ss for ss in mot_sep if ss.strip()]
            new_mot = (" ").join([ss for ss in mot_sep if ss not in ponctuations])
            new_label_preproc[j] = new_mot
        return new_label_preproc
