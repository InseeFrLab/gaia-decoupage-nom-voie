from typing import List

from voie_classes.decoupage_voie import DecoupageVoie


class FindComplement():
    def execute(self,
                 voie: DecoupageVoie,
                 types_complement: list):
        for type_compl in types_complement:  # parcours de la liste de types "complément"
            if type_compl in voie.infolib.label_preproc:
                position_type = voie.infolib.label_preproc.index(type_compl)
                positions = (position_type, position_type)
                voie.infolib.types_and_positions[(type_compl, 1)] = positions
                return True
