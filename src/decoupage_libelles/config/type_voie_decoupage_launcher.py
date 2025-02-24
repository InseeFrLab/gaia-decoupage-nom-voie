import logging
from typing import List
import pandas as pd
import json

from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from decoupage_libelles.handle_voies_no_type.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_two_types_and_more.usecase.two_types_and_more_voies_handler_use_case import TwoTypesAndMoreVoiesHandlerUseCase
from decoupage_libelles.config.settings_configuration import settings


class TypeVoieDecoupageLauncher:
    def __init__(
        self,
        voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = VoieLibPreprocessorUseCase(),
        no_type_voies_handler_use_case: NoTypeVoiesHandlerUseCase = NoTypeVoiesHandlerUseCase(),
        one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = OneTypeVoiesHandlerUseCase(),
        two_types_and_more_voies_handler_use_case: TwoTypesAndMoreVoiesHandlerUseCase = TwoTypesAndMoreVoiesHandlerUseCase(),
    ):
        self.voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = voie_lib_preprocessor_use_case
        self.no_type_voies_handler_use_case: NoTypeVoiesHandlerUseCase = no_type_voies_handler_use_case
        self.one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = one_type_voies_handler_use_case
        self.two_types_and_more_voies_handler_use_case: TwoTypesAndMoreVoiesHandlerUseCase = two_types_and_more_voies_handler_use_case

    def execute(self, voies_data: List[str]) -> List[VoieDecoupee]:
        logging.info("Préparation des données")

        logging.info("Récuperation des données 'types de voie'")
        type_voie_df = pd.read_csv(settings.chemin_type_voie)
        with open(settings.chemin_code2lib, "r", encoding="utf-8") as f:
            code2lib = json.load(f)
        logging.info("Done")

        logging.info("Preprocessing des libellés de voie donnés en entrée")
        voies_objects = [InfoVoie(label_origin=voie) for voie in voies_data]
        voies_prepared = self.voie_lib_preprocessor_use_case.execute(voies_objects, type_voie_df, code2lib)
        logging.info("Done")

        voies_processed = []

        voies_0 = [voie for voie in voies_prepared if len(voie.types_and_positions) == 0]
        voies_1 = [voie for voie in voies_prepared if len(voie.types_and_positions) == 1]
        voies_2_and_more = [voie for voie in voies_prepared if len(voie.types_and_positions) >= 2]
        logging.info("Preprocessing fini")

        logging.info("Algorithme de découpage de libellés de voie")

        logging.info("Processing des voies sans type détecté")
        if voies_0:
            voies_proc_0 = self.no_type_voies_handler_use_case.execute(voies_0)
            voies_processed += voies_proc_0
        logging.info("Done")

        logging.info("Processing des voies avec un seul type détecté")
        if voies_1:
            voies_proc_1 = self.one_type_voies_handler_use_case.execute(voies_1)
            voies_processed += voies_proc_1
        logging.info("Done")

        logging.info("Processing des voies avec deux types détectés ou plus")
        if voies_2_and_more:
            voies_proc_2_and_more = self.two_types_and_more_voies_handler_use_case.execute(voies_2_and_more)
            voies_processed += voies_proc_2_and_more
        logging.info("Done")

        return voies_processed
