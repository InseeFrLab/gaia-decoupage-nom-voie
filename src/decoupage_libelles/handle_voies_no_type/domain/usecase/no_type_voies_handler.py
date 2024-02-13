from typing import List
from tqdm import tqdm
from injector import inject
import logging

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from finders.find_complement.domain.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase
from handle_voies_no_type.domain.usecase.handle_no_type_complement import HandleNoTypeCompl
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase


class NoTypeVoiesHandler():
    @inject
    def __init__(self,
                 apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase,
                 handle_no_type_complement: HandleNoTypeCompl,
                 assign_lib_use_case: AssignLibUseCase):
        self.apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = apply_complement_finder_on_voies_use_case
        self.handle_no_type_complement: HandleNoTypeCompl = handle_no_type_complement
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) == 0]
        logging.info("Gestion des voies avec complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(
                                            voies,
                                            ComplementFinderUseCase.TYPES_COMPLEMENT_0
                                            )
        voies_treated = []
        for voie_compl in tqdm(voies_complement):
            voies_treated.append(self.handle_no_type_complement.execute(voie_compl))

        logging.info("Gestion du reste des voies")
        for voie in tqdm(voies):
            # 'LES HARDONNIERES'
            # lib
            voies_treated.append(self.assign_lib_use_case.execute(voie))

        return voies_treated
