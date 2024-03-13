from typing import List
from tqdm import tqdm
import logging

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.type_is_longitudinal_or_agglomerant_use_case import TypeIsLongitudinalOrAgglomerantUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.handle_voies_one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_two_types.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase


class ThreeTypesAndMoreVoiesHandlerUseCase:
    def __init__(
        self,
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = OneTypeVoiesHandlerUseCase(),
        two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = TwoTypesVoiesHandlerUseCase(),
    ):
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = one_type_voies_handler_use_case
        self.two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = two_types_voies_handler_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) >= 3]
        logging.info("Gestion des voies avec trois types ou plus")
        voies_treated: List[VoieDecoupee] = []
        voies_0_long_agglo: List[InfoVoie] = []
        voies_one_and_more_long_agglo: List[InfoVoie] = []
        for voie in tqdm(voies):
            types_and_positions = {
                type_and_occurence: positions
                for type_and_occurence, positions in voie.types_and_positions.items()
                if type_and_occurence[0] in TypeIsLongitudinalOrAgglomerantUseCase.TYPESLONGITUDINAUX2 + TypeIsLongitudinalOrAgglomerantUseCase.TYPESAGGLOMERANTS
            }
            if len(types_and_positions) > 0:
                voie.types_and_positions = types_and_positions
                voies_one_and_more_long_agglo.append(voie)

            else:
                voies_0_long_agglo.append(voie)

        voies_1_long_agglo = [voie for voie in voies_one_and_more_long_agglo if len(voie.types_and_positions) == 1]
        voies_2_long_agglo = [voie for voie in voies_one_and_more_long_agglo if len(voie.types_and_positions) == 2]
        voies_3_and_more_long_agglo = [voie for voie in voies_one_and_more_long_agglo if len(voie.types_and_positions) >= 3]

        if voies_0_long_agglo:
            for voie in voies_0_long_agglo:
                voie = self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)
                if voie.has_type_in_first_pos:
                    first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
                    voies_treated.append(self.assign_type_lib_use_case.execute(voie, first_type))
                else:
                    # lib
                    voies_treated.append(self.assign_lib_use_case.execute(voie))

        if voies_1_long_agglo:
            voies_proc_1_long_agglo = self.one_type_voies_handler_use_case.execute(voies_1_long_agglo)
            voies_treated += voies_proc_1_long_agglo

        if voies_2_long_agglo:
            voies_proc_2_long_agglo = self.two_types_voies_handler_use_case.execute(voies_2_long_agglo)
            voies_treated += voies_proc_2_long_agglo

        if voies_3_and_more_long_agglo:
            for voie in voies_3_and_more_long_agglo:
                # lib
                voies_treated.append(self.assign_lib_use_case.execute(voie))

        return voies_treated
