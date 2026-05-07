from typing import List
import logging

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.handlers.one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handlers.two_types.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase
from decoupage_libelles.handlers.two_types_and_more.usecase.keep_types_without_article_adj_before_use_case import KeepTypesWithoutArticleAdjBeforeUseCase
from decoupage_libelles.information_generators.type_in_lib.usecase.type_is_longitudinal_or_agglomerant_use_case import TypeIsLongitudinalOrAgglomerantUseCase
from decoupage_libelles.preprocessing.pipeline.usecase.suppress_article_in_first_place_use_case import SuppressArticleInFirstPlaceUseCase


# Types retenus lors du filtrage quand plus de 2 types détectés
_TYPES_LONG_AGGLO = (
    TypeIsLongitudinalOrAgglomerantUseCase.TYPESLONGITUDINAUX2
    + TypeIsLongitudinalOrAgglomerantUseCase.TYPESAGGLOMERANTS
)


class TwoTypesAndMoreVoiesHandlerUseCase:
    """
    Gère les voies avec 2 types ou plus détectés initialement.

    Pipeline :
    1. Suppression article initial + filtrage NLP (garde uniquement les types sans
       article/adjectif devant) → réduit le nombre de types.
    2. Reroutage selon le nombre de types restants (0, 1, 2, ou 3+).
    3. Pour 3+ types : second filtrage ne gardant que long/agglo, puis reroutage.
    """

    def __init__(
        self,
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = OneTypeVoiesHandlerUseCase(),
        two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = TwoTypesVoiesHandlerUseCase(),
        keep_types_without_article_adj_before_use_case: KeepTypesWithoutArticleAdjBeforeUseCase = KeepTypesWithoutArticleAdjBeforeUseCase(),
        suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = SuppressArticleInFirstPlaceUseCase(),
    ):
        self.assign_lib_use_case = assign_lib_use_case
        self.generate_information_on_lib_use_case = generate_information_on_lib_use_case
        self.one_type_voies_handler_use_case = one_type_voies_handler_use_case
        self.two_types_voies_handler_use_case = two_types_voies_handler_use_case
        self.keep_types_without_article_adj_before_use_case = keep_types_without_article_adj_before_use_case
        self.suppress_article_in_first_place_use_case = suppress_article_in_first_place_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) >= 2]
        logging.info("2+ types — filtrage initial par NLP")

        voies_0: List[InfoVoie] = []
        voies_1: List[InfoVoie] = []
        voies_2: List[InfoVoie] = []
        voies_treated: List[VoieDecoupee] = []

        for voie in voies:
            voie = self.suppress_article_in_first_place_use_case.execute(voie)
            voie = self.keep_types_without_article_adj_before_use_case.execute(voie)
            voie = self.generate_information_on_lib_use_case.execute(voie)
            self._route(voie, voies_0, voies_1, voies_2, voies_treated, second_pass=False)

        self._dispatch(voies_0, voies_1, voies_2, voies_treated)
        return voies_treated

    def _route(
        self,
        voie: InfoVoie,
        voies_0: List[InfoVoie],
        voies_1: List[InfoVoie],
        voies_2: List[InfoVoie],
        voies_treated: List[VoieDecoupee],
        second_pass: bool,
    ) -> None:
        n = len(voie.types_and_positions)
        if n == 0:
            voies_0.append(voie)
        elif n == 1:
            voies_1.append(voie)
        elif n == 2:
            voies_2.append(voie)
        else:
            if second_pass:
                # Fallback final : on ne garde que long/agglo et on reroutage
                voie.types_and_positions = {
                    k: v for k, v in voie.types_and_positions.items()
                    if k[0] in _TYPES_LONG_AGGLO
                }
                voie = self.generate_information_on_lib_use_case.execute(voie)
                self._route(voie, voies_0, voies_1, voies_2, voies_treated, second_pass=True)
            else:
                # 3+ types après 1er filtrage : second filtrage long/agglo uniquement
                voie.types_and_positions = {
                    k: v for k, v in voie.types_and_positions.items()
                    if k[0] in _TYPES_LONG_AGGLO
                }
                voie = self.generate_information_on_lib_use_case.execute(voie)
                self._route(voie, voies_0, voies_1, voies_2, voies_treated, second_pass=True)

    def _dispatch(
        self,
        voies_0: List[InfoVoie],
        voies_1: List[InfoVoie],
        voies_2: List[InfoVoie],
        voies_treated: List[VoieDecoupee],
    ) -> None:
        for voie in voies_0:
            voies_treated.append(self.assign_lib_use_case.execute(voie))
        if voies_1:
            voies_treated += self.one_type_voies_handler_use_case.execute(voies_1)
        if voies_2:
            voies_treated += self.two_types_voies_handler_use_case.execute(voies_2)
