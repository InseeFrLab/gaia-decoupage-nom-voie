from typing import List
from tqdm import tqdm

from voie_classes.decoupage_voie import DecoupageVoie


class ThreeMoreTypesVoiesHandler():
    def __init__(self,
                 voies: List[DecoupageVoie]):
        self.voies = [voie for voie in voies if (voie.infolib.nb_types_detected() >= 3 and
                                                 voie.not_assigned())]

    def handle_voies(self):
        # Pas de règles de décision développées
        for voie in tqdm(self.voies):
            voie.assign_lib()

    def run(self):
        print("Gestion des voies")
        self.handle_voies()
        return self.voies
