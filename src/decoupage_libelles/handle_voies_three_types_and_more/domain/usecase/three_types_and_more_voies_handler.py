from typing import List
from tqdm import tqdm
from injector import inject
import logging

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase

class ThreeTypesAndMoreVoiesHandler():
    @inject
    def __init__(self,
                 assign_lib_use_case: AssignLibUseCase):
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) >= 3]
        logging.info("Gestion des voies avec trois types ou plus")
        voies_treated = []
        for voie_fictive in tqdm(voies):
            # 'LES VERNONS RUE B'
            # lib + compl
            voies_treated.append(self.assign_lib_use_case.execute(voie_fictive))
        return voies_treated
