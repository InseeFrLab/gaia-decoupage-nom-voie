import logging
from injector import inject
from typing import List

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from prepare_data.clean_type_voie.domain.usecase.type_voie_majic_preprocessor_use_case import TypeVoieMajicPreprocessorUseCase
from prepare_data.clean_voie_lib_and_find_types.domain.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from handle_voies_no_type.domain.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from handle_voies_one_type.domain.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from handle_voies_two_types.domain.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase
from handle_voies_three_types_and_more.domain.usecase.three_types_and_more_voies_handler_use_case import ThreeTypesAndMoreVoiesHandlerUseCase


class TypeVoieDecoupageLauncher:
    @inject
    def __init__(self, type_voie_majic_preprocessor_use_case: TypeVoieMajicPreprocessorUseCase,
                 voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase,
                 no_type_voies_handler_use_case: NoTypeVoiesHandlerUseCase,
                 one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase,
                 two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase,
                 three_types_and_more_voies_handler_use_case: ThreeTypesAndMoreVoiesHandlerUseCase):
        self.type_voie_majic_preprocessor_use_case: TypeVoieMajicPreprocessorUseCase = type_voie_majic_preprocessor_use_case
        self.voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = voie_lib_preprocessor_use_case
        self.no_type_voies_handler_use_case: NoTypeVoiesHandlerUseCase = no_type_voies_handler_use_case
        self.one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = one_type_voies_handler_use_case
        self.two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = two_types_voies_handler_use_case
        self.three_types_and_more_voies_handler_use_case: ThreeTypesAndMoreVoiesHandlerUseCase = three_types_and_more_voies_handler_use_case

    def execute(self, voies_data) -> List[VoieDecoupee]:
        logging.info('Préparation des données')

        logging.info("Preprocessing des données 'types de voie' issues de Majic")
        type_voie_df, code2lib = self.type_voie_majic_preprocessor_use_case.execute()
        logging.info("Done")

        logging.info("Preprocessing des libellés de voie donnés en entrée")
        voies_objects = [InfoVoie(voie) for voie in voies_data]
        voies_prepared = self.voie_lib_preprocessor_use_case.execute(voies_objects, type_voie_df, code2lib)
        logging.info("Done")

        voies_0 = [voie for voie in voies_prepared if len(voie.types_and_positions) == 0]
        voies_1 = [voie for voie in voies_prepared if len(voie.types_and_positions) == 1]
        voies_2 = [voie for voie in voies_prepared if len(voie.types_and_positions) == 2]
        voies_3_and_more = [voie for voie in voies_prepared if len(voie.types_and_positions) >= 3]

        logging.info('Preprocessing fini')

        logging.info('Algorithme de découpage de libellés de voie')

        voies_processed = []

        logging.info('Processing des voies sans type détecté')
        if voies_0: 
            voies_proc_0 = self.no_type_voies_handler_use_case.execute(voies_0)
            voies_processed.append(voies_proc_0)
        logging.info("Done")

        logging.info('Processing des voies avec un seul type détecté')
        if voies_1:
            voies_proc_1 = self.one_type_voies_handler_use_case.execute(voies_1)
            voies_processed.append(voies_proc_1)
        logging.info("Done")

        logging.info('Processing des voies avec deux types détectés')
        if voies_2:
            voies_proc_2 = self.two_types_voies_handler_use_case.execute(voies_2)
            voies_processed.append(voies_proc_2)
        logging.info("Done")

        logging.info('Processing des voies avec trois types détectés ou plus')
        if voies_3_and_more:
            voies_proc_3_and_more = self.three_types_and_more_voies_handler_use_case.execute(voies_3_and_more)
            voies_processed.append(voies_proc_3_and_more)
        logging.info("Done")

        return voies_processed