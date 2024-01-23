from typing import List
from tqdm import tqdm

from voie_classes.decoupage_voie import DecoupageVoie
from finders.complement_finder import ComplementFinder
from finders.voie_fictive_finder import VoieFictiveFinder
from processors.one_type.one_type_assign_voies_complement import OneTypeAssignCompl
from processors.one_type.one_type_assign_voies_type_not_first_pos import OneTypeAssignNotFirstPos
from constants.constant_lists import (liste_types_complement_1,
                                      liste_voie_fictive_1
                                      )


class OneTypeVoiesHandler():
    def __init__(self,
                 voies: List[DecoupageVoie]):
        self.voies = [voie for voie in voies if (voie.infolib.nb_types_detected() == 1 and
                                                 voie.not_assigned())]
        self.voies_complement = None
        self.voies_fictives = None

    def handle_voies_complementaires(self):
        self.voies_complement, self.voies = ComplementFinder.apply_find_type_complement_on_list(
                                            self.voies,
                                            liste_types_complement_1
                                            )

        for voie_compl in tqdm(self.voies_complement):
            OneTypeAssignCompl(voie_compl).run()

    def handle_voies_fictives(self):
        self.voies_fictives, self.voies = VoieFictiveFinder.apply_find_voies_fictives_on_list(
                                          self.voies,
                                          liste_voie_fictive_1
                                          )

        # test = VoieType('LES VERNONS RUE B', ['LES', 'VERNONS', 'RUE', 'B'], ['RUE'], [2])
        # test.find_voies_fictives(liste_voie_fictive)

        for voie_fictive in tqdm(self.voies_fictives):
            # 'LES VERNONS RUE B'
            # lib + compl
            voie_fictive.assign_lib_compl()

    def handle_voies_not_compl_not_fictives(self):
        for voie in tqdm(self.voies):
            if voie.has_type_in_first_pos():
                # 1er type + lib
                # test = VoieType('CHE DES SEMAPHORES', ['CHE', 'DES', 'SEMAPHORES'], ['CHEMIN'], [0], [])
                voie.assign_type_lib(1)

            else:
                OneTypeAssignNotFirstPos(voie).run()

    def run(self):
        print("Gestion des voies avec complément")
        self.handle_voies_complementaires()
        print("Gestion des voies fictives")
        self.handle_voies_fictives()
        print("Gestion du reste des voies")
        self.handle_voies_not_compl_not_fictives()
        voies_traited = self.voies + self.voies_complement + self.voies_fictives
        return voies_traited
