import logging
from typing import List

from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.preprocessing.pipeline.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from decoupage_libelles.handlers.no_type.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from decoupage_libelles.handlers.one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handlers.two_types_and_more.usecase.two_types_and_more_voies_handler_use_case import TwoTypesAndMoreVoiesHandlerUseCase


class TypeVoieDecoupageLauncher:
    """
    Orchestrateur principal du découpage.

    Simplifications vs version précédente :
    - TypeFinderUtils chargé une seule fois dans __init__ (plus de lecture CSV
      à chaque appel à execute()).
    - Routage exprimé en une compréhension de liste par branche, sans if/else.
    """

    def __init__(
        self,
        voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = VoieLibPreprocessorUseCase(),
        no_type_voies_handler_use_case: NoTypeVoiesHandlerUseCase = NoTypeVoiesHandlerUseCase(),
        one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = OneTypeVoiesHandlerUseCase(),
        two_types_and_more_voies_handler_use_case: TwoTypesAndMoreVoiesHandlerUseCase = TwoTypesAndMoreVoiesHandlerUseCase(),
    ):
        self.voie_lib_preprocessor_use_case = voie_lib_preprocessor_use_case
        self.no_type_voies_handler_use_case = no_type_voies_handler_use_case
        self.one_type_voies_handler_use_case = one_type_voies_handler_use_case
        self.two_types_and_more_voies_handler_use_case = two_types_and_more_voies_handler_use_case

    def execute(self, voies_data: List[str]) -> List[VoieDecoupee]:
        logging.info("Preprocessing des libellés")
        voies_objects = [InfoVoie(label_origin=voie) for voie in voies_data]
        voies_prepared = self.voie_lib_preprocessor_use_case.execute(
            voies_objects
        )

        voies_0        = [v for v in voies_prepared if len(v.types_and_positions) == 0]
        voies_1        = [v for v in voies_prepared if len(v.types_and_positions) == 1]
        voies_2_plus   = [v for v in voies_prepared if len(v.types_and_positions) >= 2]

        voies_processed: List[VoieDecoupee] = []

        logging.info(f"Voies sans type   : {len(voies_0)}")
        if voies_0:
            voies_processed += self.no_type_voies_handler_use_case.execute(voies_0)

        logging.info(f"Voies avec 1 type : {len(voies_1)}")
        if voies_1:
            voies_processed += self.one_type_voies_handler_use_case.execute(voies_1)

        logging.info(f"Voies avec 2+ types : {len(voies_2_plus)}")
        if voies_2_plus:
            voies_processed += self.two_types_and_more_voies_handler_use_case.execute(voies_2_plus)

        return voies_processed
