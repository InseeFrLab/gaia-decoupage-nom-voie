from typing import List
import logging

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.finders.find_complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.handle_voies_no_type.usecase.handle_no_type_complement_use_case import HandleNoTypeComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase


class NoTypeVoiesHandlerUseCase:
    def __init__(
        self,
        apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = ApplyComplementFinderOnVoiesUseCase(),
        handle_no_type_complement_use_case: HandleNoTypeComplUseCase = HandleNoTypeComplUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
        self.apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = apply_complement_finder_on_voies_use_case
        self.handle_no_type_complement_use_case: HandleNoTypeComplUseCase = handle_no_type_complement_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        logging.info("Gestion des voies avec complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(voies, ComplementFinderUseCase.TYPES_COMPLEMENT_0)
        voies_treated = []
        for voie_compl in voies_complement:
            voies_treated.append(self.handle_no_type_complement_use_case.execute(voie_compl))

        logging.info("Gestion du reste des voies")
        for voie in voies:
            # 'LES HARDONNIERES'
            # lib
            voies_treated.append(self.assign_lib_use_case.execute(voie))

        return voies_treated
