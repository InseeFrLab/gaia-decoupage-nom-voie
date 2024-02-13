from typing import List
from tqdm import tqdm
from injector import inject
import logging

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from finders.find_complement.domain.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from finders.find_voie_fictive.domain.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase
from finders.find_voie_fictive.domain.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase
from handle_voies_one_type.domain.usecase.handle_one_type_complement import HandleOneTypeCompl
from handle_voies_one_type.domain.usecase.handle_one_type_not_compl_not_fictif import HandleOneTypeNotComplNotFictif
from decoupe_voie.domain.usecase.assign_lib_compl_use_case import AssignLibComplUseCase

class OneTypeVoiesHandler():
    @inject
    def __init__(self,
                 apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase,
                 apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase,
                 handle_one_type_complement: HandleOneTypeCompl,
                 handle_one_type_not_compl_not_fictif: HandleOneTypeNotComplNotFictif,
                 assign_lib_compl_use_case: AssignLibComplUseCase):
        self.apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = apply_complement_finder_on_voies_use_case
        self.apply_voie_fictive_finder_on_voies_use_case: ApplyVoieFictiveFinderOnVoiesUseCase = apply_voie_fictive_finder_on_voies_use_case
        self.handle_one_type_complement: HandleOneTypeCompl = handle_one_type_complement
        self.handle_one_type_not_compl_not_fictif: HandleOneTypeNotComplNotFictif = handle_one_type_not_compl_not_fictif
        self.assign_lib_compl_use_case: AssignLibComplUseCase = assign_lib_compl_use_case

    def execute(self, voies: List[InfoVoie]) -> List[VoieDecoupee]:
        voies = [voie for voie in voies if len(voie.types_and_positions) == 1]
        logging.info("Gestion des voies avec complément")
        voies_complement, voies = self.apply_complement_finder_on_voies_use_case.execute(
                                            voies,
                                            ComplementFinderUseCase.TYPES_COMPLEMENT_1_2
                                            )
        voies_treated = []
        for voie_compl in tqdm(voies_complement):
            voies_treated.append(self.handle_one_type_complement.execute(voie_compl))

        logging.info("Gestion des voies fictives")
        voies_fictives, voies = self.apply_voie_fictive_finder_on_voies_use_case.execute(
                                          voies,
                                          VoieFictiveFinderUseCase.VOIES_FICTIVES_1
                                          )
        for voie_fictive in tqdm(voies_fictives):
            # 'LES VERNONS RUE B'
            # lib + compl
            voies_treated.append(self.assign_lib_compl_use_case.execute(voie_fictive))

        logging.info("Gestion du reste des voies")
        for voie in tqdm(voies):
            voies_treated.append(self.handle_one_type_not_compl_not_fictif.execute(voie))

        return voies_treated
