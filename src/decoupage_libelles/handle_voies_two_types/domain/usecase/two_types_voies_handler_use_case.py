from typing import List
from tqdm import tqdm
from injector import inject
import logging

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from finders.find_complement.domain.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from finders.find_voie_fictive.domain.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase
from finders.find_voie_fictive.domain.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase
from handle_voies_two_types.domain.usecase.handle_two_types_complement_use_case import HandleTwoTypesComplUseCase
from handle_voies_two_types.domain.usecase.handle_two_types_voie_fictive_use_case import HandleTwoTypesVoieFictiveUseCase
from handle_voies_two_types.domain.usecase.handle_has_type_in_first_pos_use_case import HandleHasTypeInFirstPosUseCase
from handle_voies_two_types.domain.usecase.handle_no_type_in_first_pos_use_case import HandleNoTypeInFirstPosUseCase


class TwoTypesVoiesHandlerUseCase:
    @inject
    def __init__(self,
                 apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase,
                 apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase,
                 handle_two_types_complement_use_case: HandleTwoTypesComplUseCase,
                 handle_two_types_voie_fictive_use_case: HandleTwoTypesVoieFictiveUseCase,
                 handle_has_type_in_first_pos_use_case: HandleHasTypeInFirstPosUseCase,
                 handle_no_type_in_first_pos_use_case: HandleNoTypeInFirstPosUseCase,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase):
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
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(
                                            voies,
                                            ComplementFinderUseCase.TYPES_COMPLEMENT_1_2
                                            )
        voies_treated = []
        for voie_compl in tqdm(voies_complement):
            voie_treated, voie_to_treat_two_types = self.handle_two_types_complement_use_case.execute(voie_compl)
            if voie_treated:
                voies_treated.append(voie_treated)
            else:
                voies.append(voie_to_treat_two_types)

        logging.info("Gestion des voies fictives")
        voies_fictives, voies = self.apply_voie_fictive_finder_on_voies_use_case.execute(
                                          voies,
                                          VoieFictiveFinderUseCase.VOIES_FICTIVES_2
                                          )
        for voie_fictive in tqdm(voies_fictives):
            voies_treated.append(self.handle_two_types_voie_fictive_use_case.execute(voie_fictive))

        for voie in tqdm(voies):
            self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)
            if voie.has_type_in_first_pos:
                logging.info("Gestion des voies avec un type en première position")
                logging.info("Étape longue")
                voie_treated = self.handle_has_type_in_first_pos_use_case.execute(voie)
            else:
                logging.info("Gestion des voies sans type en première position")
                voie_treated = self.handle_no_type_in_first_pos_use_case.execute(voie) if not voie_treated else voie_treated

            voies_treated.append(voie_treated)

        return voies_treated
