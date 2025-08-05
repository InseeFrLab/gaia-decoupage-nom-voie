from typing import List
import logging

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.handle_voies_one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_two_types.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase
from decoupage_libelles.handle_voies_two_types_and_more.usecase.keep_types_without_article_adj_before_use_case import KeepTypesWithoutArticleAdjBeforeUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.type_is_longitudinal_or_agglomerant_use_case import TypeIsLongitudinalOrAgglomerantUseCase
from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.suppress_article_in_first_place_use_case import SuppressArticleInFirstPlaceUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase


class TwoTypesAndMoreVoiesHandlerUseCase:
    def __init__(
        self,
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = OneTypeVoiesHandlerUseCase(),
        two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = TwoTypesVoiesHandlerUseCase(),
        keep_types_without_article_adj_before_use_case: KeepTypesWithoutArticleAdjBeforeUseCase = KeepTypesWithoutArticleAdjBeforeUseCase(),
        suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = SuppressArticleInFirstPlaceUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
    ):
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = one_type_voies_handler_use_case
        self.two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = two_types_voies_handler_use_case
        self.keep_types_without_article_adj_before_use_case: KeepTypesWithoutArticleAdjBeforeUseCase = keep_types_without_article_adj_before_use_case
        self.suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = suppress_article_in_first_place_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) >= 2]
        logging.info("Gestion des voies avec trois types ou plus")
        voies_treated: List[VoieDecoupee] = []
        voies_0_long_agglo: List[InfoVoie] = []
        voies_1_long_agglo: List[InfoVoie] = []
        voies_2_long_agglo: List[InfoVoie] = []

        for voie in voies:
            voie = self.suppress_article_in_first_place_use_case.execute(voie)
            voie = self.keep_types_without_article_adj_before_use_case.execute(voie)
            voie = self.generate_information_on_lib_use_case.execute(voie)

            if len(voie.types_and_positions) == 0:
                voies_0_long_agglo.append(voie)
            elif len(voie.types_and_positions) == 1:
                voies_1_long_agglo.append(voie)
            elif len(voie.types_and_positions) == 2:
                voies_2_long_agglo.append(voie)
            else:
                voie.types_and_positions = {
                    type_and_occurence: positions
                    for type_and_occurence, positions in voie.types_and_positions.items()
                    if type_and_occurence[0] in TypeIsLongitudinalOrAgglomerantUseCase.TYPESLONGITUDINAUX2 + TypeIsLongitudinalOrAgglomerantUseCase.TYPESAGGLOMERANTS
                }
                voie = self.generate_information_on_lib_use_case.execute(voie)

                if len(voie.types_and_positions) == 0:
                    voies_0_long_agglo.append(voie)
                elif len(voie.types_and_positions) == 1:
                    voies_1_long_agglo.append(voie)
                elif len(voie.types_and_positions) == 2:
                    voies_2_long_agglo.append(voie)
                else:
                    # lib
                    voies_treated.append(self.assign_lib_use_case.execute(voie))

        # logging.info(f"voies0 : {[voie for voie in voies_0_long_agglo]}")
        # logging.info(f"voies1 : {[voie for voie in voies_1_long_agglo]}")
        # logging.info(f"voies2 : {[voie for voie in voies_2_long_agglo]}")

        if voies_0_long_agglo:
            for voie in voies_0_long_agglo:
                # lib
                voies_treated.append(self.assign_lib_use_case.execute(voie))

        if voies_1_long_agglo:
            voies_proc_1_long_agglo = self.one_type_voies_handler_use_case.execute(voies_1_long_agglo)
            voies_treated += voies_proc_1_long_agglo

        if voies_2_long_agglo:
            voies_proc_2_long_agglo = self.two_types_voies_handler_use_case.execute(voies_2_long_agglo)
            voies_treated += voies_proc_2_long_agglo

        return voies_treated
