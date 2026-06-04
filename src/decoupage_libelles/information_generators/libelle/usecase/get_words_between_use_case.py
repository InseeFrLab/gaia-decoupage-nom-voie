from typing import Optional

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie


class GetWordsBetweenUseCase:
    def execute(
        self,
        infovoie: InfoVoie,
        position_start: int,
        position_end: Optional[int] = None
    ) -> Optional[str]:
        if position_end and len(infovoie.label_preproc) >= position_end:
            return (" ").join(infovoie.label_preproc[position_start:position_end])
        elif position_end is None and len(infovoie.label_preproc) > position_start:
            return (" ").join(infovoie.label_preproc[position_start:])
        else:
            return ""
