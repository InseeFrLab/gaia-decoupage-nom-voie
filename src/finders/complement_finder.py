from typing import List
from tqdm import tqdm

from voie_classes.decoupage_voie import DecoupageVoie


class ComplementFinder():
    def __init__(self,
                 voie: DecoupageVoie,
                 types_complement: list):
        self.voie = voie
        self.types_complement = types_complement
        self.has_type_compl = False

    def find_complement(self):
        for type_compl in self.types_complement:  # parcours de la liste de types "complément"
            if type_compl in self.voie.infolib.label_preproc:
                position_type = self.voie.infolib.label_preproc.index(type_compl)
                positions = (position_type, position_type)
                self.voie.infolib.types_and_positions[(type_compl, 1)] = positions
                self.has_type_compl = True

    def run(self):
        self.find_complement()
        if self.has_type_compl:
            self.voie.infolib.sort_types_by_position()
            return self.voie

    @staticmethod
    def apply_find_type_complement_on_list(
            voies_obj: List[DecoupageVoie],
            types_to_detect: list,
            ):

        voies_obj_compl = []
        new_voies_obj = voies_obj[:]
        for voie in tqdm(voies_obj):
            new_voie = ComplementFinder(voie, types_to_detect).run()
            if new_voie:
                voies_obj_compl.append(new_voie)
                new_voies_obj.remove(voie)

        return (voies_obj_compl, new_voies_obj)
