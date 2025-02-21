from typing import List


class ListIsIncludedInOtherListUseCase:
    def execute(self, petite_liste: List[str], grande_liste: List[str]) -> bool:
        if not petite_liste:
            return False

        len_petite = len(petite_liste)
        len_grande = len(grande_liste)

        for i in range(len_grande - len_petite + 1):
            if grande_liste[i : i + len_petite] == petite_liste:
                return True

        return False
