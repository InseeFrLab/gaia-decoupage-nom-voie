from typing import List
import logging

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.finders.complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.finders.voie_fictive.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase
from decoupage_libelles.synonym_data.voies_fictives import VOIES_FICTIVES_2
from decoupage_libelles.handlers.two_types.usecase.handle_two_types_complement_use_case import HandleTwoTypesComplUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_two_types_voie_fictive_use_case import HandleTwoTypesVoieFictiveUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_has_type_in_first_pos_use_case import HandleHasTypeInFirstPosUseCase
from decoupage_libelles.handlers.two_types.usecase.handle_no_type_in_first_pos_use_case import HandleNoTypeInFirstPosUseCase
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.synonym_data.complement_types import TYPES_COMPLEMENT


class TwoTypesVoiesHandlerUseCase:
    def __init__(
        self,
        apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = ApplyComplementFinderOnVoiesUseCase(),
        apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = ApplyVoieFictiveFinderOnVoiesUseCase(),
        handle_two_types_complement_use_case: HandleTwoTypesComplUseCase = HandleTwoTypesComplUseCase(),
        handle_two_types_voie_fictive_use_case: HandleTwoTypesVoieFictiveUseCase = HandleTwoTypesVoieFictiveUseCase(),
        handle_has_type_in_first_pos_use_case: HandleHasTypeInFirstPosUseCase = HandleHasTypeInFirstPosUseCase(),
        handle_no_type_in_first_pos_use_case: HandleNoTypeInFirstPosUseCase = HandleNoTypeInFirstPosUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
    ):
        self.apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = apply_complement_finder_on_voies_use_case
        self.apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = apply_voie_fictive_finder_on_voies_use_case
        self.handle_two_types_complement_use_case: HandleTwoTypesComplUseCase = handle_two_types_complement_use_case
        self.handle_two_types_voie_fictive_use_case: HandleTwoTypesVoieFictiveUseCase = handle_two_types_voie_fictive_use_case
        self.handle_has_type_in_first_pos_use_case: HandleHasTypeInFirstPosUseCase = handle_has_type_in_first_pos_use_case
        self.handle_no_type_in_first_pos_use_case: HandleNoTypeInFirstPosUseCase = handle_no_type_in_first_pos_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) == 2]

        logging.info("Gestion des voies avec complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(voies, TYPES_COMPLEMENT)
        voies_treated = []
        for voie_compl in voies_complement:
            voie_treated, voie_to_treat_two_types = self.handle_two_types_complement_use_case.execute(voie_compl)
            if voie_treated:
                voies_treated.append(voie_treated)
            else:
                voies.append(voie_to_treat_two_types)

        logging.info("Gestion des voies fictives")
        voies_fictives, voies = self.apply_voie_fictive_finder_on_voies_use_case.execute(voies, VOIES_FICTIVES_2)
        for voie_fictive in voies_fictives:
            voies_treated.append(self.handle_two_types_voie_fictive_use_case.execute(voie_fictive))

        for voie in voies:
            voie_treated = None
            if voie.has_type_in_first_pos:
                logging.info("Gestion des voies avec un type en première position")
                logging.info("Étape longue")
                voie_treated = self.handle_has_type_in_first_pos_use_case.execute(voie)
            else:
                logging.info("Gestion des voies sans type en première position")
                voie_treated = self.handle_no_type_in_first_pos_use_case.execute(voie) if not voie_treated else voie_treated

            voies_treated.append(voie_treated)

        return voies_treated
