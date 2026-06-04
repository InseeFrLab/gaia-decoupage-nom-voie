from typing import List

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie


class ComplementFinderUseCase:
    def execute(self, infovoie: InfoVoie, types_complement: List[str]) -> InfoVoie:
        for type_compl in types_complement:  # parcours de la liste de types "complément"
            if type_compl in infovoie.label_preproc:
                position_type = infovoie.label_preproc.index(type_compl)
                positions = (position_type, position_type)
                infovoie.types_and_positions[(type_compl, 1)] = positions
                infovoie.types_and_positions = dict(sorted(infovoie.types_and_positions.items(), key=lambda x: x[1][0]))
                return infovoie
