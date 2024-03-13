from typing import List
from tqdm import tqdm
import logging

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.finders.find_complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.finders.find_voie_fictive.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase
from decoupage_libelles.finders.find_voie_fictive.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.handle_voies_one_type.usecase.handle_one_type_complement_use_case import HandleOneTypeComplUseCase
from decoupage_libelles.handle_voies_one_type.usecase.handle_one_type_not_compl_not_fictif_use_case import HandleOneTypeNotComplNotFictifUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_compl_use_case import AssignLibComplUseCase


class OneTypeVoiesHandlerUseCase:
    def __init__(
        self,
        apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = ApplyComplementFinderOnVoiesUseCase(),
        apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = ApplyVoieFictiveFinderOnVoiesUseCase(),
        handle_one_type_complement_use_case: HandleOneTypeComplUseCase = HandleOneTypeComplUseCase(),
        handle_one_type_not_compl_not_fictif_use_case: HandleOneTypeNotComplNotFictifUseCase = HandleOneTypeNotComplNotFictifUseCase(),
        assign_lib_compl_use_case: AssignLibComplUseCase = AssignLibComplUseCase(),
    ):
        self.apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = apply_complement_finder_on_voies_use_case
        self.apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = apply_voie_fictive_finder_on_voies_use_case
        self.handle_one_type_complement_use_case: HandleOneTypeComplUseCase = handle_one_type_complement_use_case
        self.handle_one_type_not_compl_not_fictif_use_case: HandleOneTypeNotComplNotFictifUseCase = handle_one_type_not_compl_not_fictif_use_case
        self.assign_lib_compl_use_case: AssignLibComplUseCase = assign_lib_compl_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) == 1]
        logging.info("Gestion des voies avec complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(voies, ComplementFinderUseCase.TYPES_COMPLEMENT_1_2)
        voies_treated = []
        for voie_compl in tqdm(voies_complement):
            voies_treated.append(self.handle_one_type_complement_use_case.execute(voie_compl))

        logging.info("Gestion des voies fictives")
        voies_fictives, voies = self.apply_voie_fictive_finder_on_voies_use_case.execute(voies, VoieFictiveFinderUseCase.VOIES_FICTIVES_1)
        for voie_fictive in tqdm(voies_fictives):
            # 'LES VERNONS RUE B'
            # lib + compl
            voies_treated.append(self.assign_lib_compl_use_case.execute(voie_fictive))

        logging.info("Gestion du reste des voies")
        for voie in tqdm(voies):
            voies_treated.append(self.handle_one_type_not_compl_not_fictif_use_case.execute(voie))

        return voies_treated
