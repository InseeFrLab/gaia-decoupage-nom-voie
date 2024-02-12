from typing import List
from tqdm import tqdm


from handle_voies_no_type.domain.usecase.no_type_handle_complement import NoTypeAssignCompl


class NoTypeVoiesHandler():
    def __init__(self,
                 voies: List[DecoupageVoie]):
        self.voies = [voie for voie in voies if voie.infolib.nb_types_detected() == 0]
        self.voies_complement = None

    def handle_voies_complementaires(self):
        self.voies_complement, self.voies = ComplementFinder.apply_find_type_complement_on_list(
                                            self.voies,
                                            liste_types_complement_0
                                            )

        for voie_compl in tqdm(self.voies_complement):
            NoTypeAssignCompl(voie_compl).run()

    def handle_voies_rest(self):
        for voie in tqdm(self.voies):
            # 'LES HARDONNIERES'
            # lib
            voie.assign_lib()

    def run(self):
        print("Gestion des voies avec complément")
        self.handle_voies_complementaires()
        print("Gestion du reste des voies")
        self.handle_voies_rest()
        voies_traited = self.voies + self.voies_complement
        return voies_traited
