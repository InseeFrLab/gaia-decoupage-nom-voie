from typing import Optional

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie


class GetWordsBetweenUseCase:

    def execute(self, infovoie: InfoVoie, position_start: int, position_end: Optional[int] = None) -> str:
        if position_end:
            if len(infovoie.label_preproc) >= position_end:
                return (' ').join(infovoie.label_preproc[position_start:position_end])
        else:
            if len(infovoie.label_preproc) > position_start:
                return (' ').join(infovoie.label_preproc[position_start:])