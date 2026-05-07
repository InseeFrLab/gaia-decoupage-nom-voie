from typing import List
import logging

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.finders.complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.finders.voie_fictive.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase
from decoupage_libelles.finders.voie_fictive.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from decoupage_libelles.finders.complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_two_types_complement_use_case import HandleTwoTypesComplUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_two_types_voie_fictive_use_case import HandleTwoTypesVoieFictiveUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_has_type_in_first_pos_use_case import HandleHasTypeInFirstPosUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_no_type_in_first_pos_use_case import HandleNoTypeInFirstPosUseCase


class TwoTypesVoiesHandlerUseCase:
    def __init__(
        self,
        apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = ApplyComplementFinderOnVoiesUseCase(),
        apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = ApplyVoieFictiveFinderOnVoiesUseCase(),
        handle_two_types_complement_use_case: HandleTwoTypesComplUseCase = HandleTwoTypesComplUseCase(),
        handle_two_types_voie_fictive_use_case: HandleTwoTypesVoieFictiveUseCase = HandleTwoTypesVoieFictiveUseCase(),
        handle_has_type_in_first_pos_use_case: HandleHasTypeInFirstPosUseCase = HandleHasTypeInFirstPosUseCase(),
        handle_no_type_in_first_pos_use_case: HandleNoTypeInFirstPosUseCase = HandleNoTypeInFirstPosUseCase(),
    ):
        self.apply_complement_finder_on_voies_use_case = apply_complement_finder_on_voies_use_case
        self.apply_voie_fictive_finder_on_voies_use_case = apply_voie_fictive_finder_on_voies_use_case
        self.handle_two_types_complement_use_case = handle_two_types_complement_use_case
        self.handle_two_types_voie_fictive_use_case = handle_two_types_voie_fictive_use_case
        self.handle_has_type_in_first_pos_use_case = handle_has_type_in_first_pos_use_case
        self.handle_no_type_in_first_pos_use_case = handle_no_type_in_first_pos_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) == 2]
        voies_treated: List[VoieDecoupee] = []

        logging.info("2 types — recherche d'un complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(
            voies, ComplementFinderUseCase.TYPES_COMPLEMENT_1_2
        )
        for voie_compl in voies_complement:
            voie_treated, voie_to_treat_two_types = self.handle_two_types_complement_use_case.execute(voie_compl)
            if voie_treated:
                voies_treated.append(voie_treated)
            else:
                voies.append(voie_to_treat_two_types)

        logging.info("2 types — recherche de voie fictive")
        voies_fictives, voies = self.apply_voie_fictive_finder_on_voies_use_case.execute(
            voies, VoieFictiveFinderUseCase.VOIES_FICTIVES_2
        )
        for voie_fictive in voies_fictives:
            voies_treated.append(self.handle_two_types_voie_fictive_use_case.execute(voie_fictive))

        logging.info("2 types — cas général")
        for voie in voies:
            # CORRECTION faille : branchement clair et déterministe, sans condition redondante
            if voie.has_type_in_first_pos:
                voie_treated = self.handle_has_type_in_first_pos_use_case.execute(voie)
            else:
                voie_treated = self.handle_no_type_in_first_pos_use_case.execute(voie)
            voies_treated.append(voie_treated)

        return voies_treated
