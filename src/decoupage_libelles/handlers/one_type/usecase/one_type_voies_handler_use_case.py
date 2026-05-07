from typing import List
import logging

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.finders.complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.finders.voie_fictive.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase
from decoupage_libelles.finders.voie_fictive.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from decoupage_libelles.finders.complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.handlers.one_type.usecase.handle_one_type_complement_use_case import HandleOneTypeComplUseCase
from decoupage_libelles.handlers.one_type.usecase.handle_one_type_not_compl_not_fictif_use_case import HandleOneTypeNotComplNotFictifUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.preprocessing.pipeline.usecase.suppress_article_in_first_place_use_case import SuppressArticleInFirstPlaceUseCase


class OneTypeVoiesHandlerUseCase:
    def __init__(
        self,
        apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = ApplyComplementFinderOnVoiesUseCase(),
        apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = ApplyVoieFictiveFinderOnVoiesUseCase(),
        handle_one_type_complement_use_case: HandleOneTypeComplUseCase = HandleOneTypeComplUseCase(),
        handle_one_type_not_compl_not_fictif_use_case: HandleOneTypeNotComplNotFictifUseCase = HandleOneTypeNotComplNotFictifUseCase(),
        assign_lib_compl_use_case: AssignLibComplUseCase = AssignLibComplUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = SuppressArticleInFirstPlaceUseCase(),
    ):
        self.apply_complement_finder_on_voies_use_case = apply_complement_finder_on_voies_use_case
        self.apply_voie_fictive_finder_on_voies_use_case = apply_voie_fictive_finder_on_voies_use_case
        self.handle_one_type_complement_use_case = handle_one_type_complement_use_case
        self.handle_one_type_not_compl_not_fictif_use_case = handle_one_type_not_compl_not_fictif_use_case
        self.assign_lib_compl_use_case = assign_lib_compl_use_case
        self.generate_information_on_lib_use_case = generate_information_on_lib_use_case
        self.suppress_article_in_first_place_use_case = suppress_article_in_first_place_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) == 1]
        voies_treated: List[VoieDecoupee] = []

        # Prétraitement commun : suppression article initial + info lib (sans NLP)
        for voie in voies:
            self.suppress_article_in_first_place_use_case.execute(voie)
            self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)

        logging.info("1 type — recherche d'un complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(
            voies, ComplementFinderUseCase.TYPES_COMPLEMENT_1_2
        )
        for voie_compl in voies_complement:
            voies_treated.append(self.handle_one_type_complement_use_case.execute(voie_compl))

        logging.info("1 type — recherche de voie fictive")
        voies_fictives, voies = self.apply_voie_fictive_finder_on_voies_use_case.execute(
            voies, VoieFictiveFinderUseCase.VOIES_FICTIVES_1
        )
        for voie_fictive in voies_fictives:
            # 'LES VERNONS RUE B' → lib + compl
            voies_treated.append(self.assign_lib_compl_use_case.execute(voie_fictive))

        logging.info("1 type — cas général")
        for voie in voies:
            voies_treated.append(self.handle_one_type_not_compl_not_fictif_use_case.execute(voie))

        return voies_treated
