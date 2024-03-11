from typing import List
from tqdm import tqdm
import logging

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase


class ThreeTypesAndMoreVoiesHandlerUseCase:
    def __init__(self, assign_lib_use_case: AssignLibUseCase = AssignLibUseCase()):
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) >= 3]
        logging.info("Gestion des voies avec trois types ou plus")
        voies_treated = []
        for voie in tqdm(voies):
            # "RESIDENCE COUR DE FERME"
            # lib
            voies_treated.append(self.assign_lib_use_case.execute(voie))
        return voies_treated
