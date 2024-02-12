from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_second_pos import ComplTypeInFirstOrSecondPos
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_middle_pos import ComplTypeInFirstOrMiddlePos
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_last_pos import ComplTypeInFirstOrLastPos
from handle_voies_one_type.domain.usecase.handle_one_type_not_first_pos import HandleOneTypeNotFirstPos

class HandleOneTypeNotComplNotFictif:
    @inject
    def __init__(self, compl_type_in_first_or_second_pos: ComplTypeInFirstOrSecondPos,
                 compl_type_in_first_or_middle_pos: ComplTypeInFirstOrMiddlePos,
                 compl_type_in_first_or_last_pos: ComplTypeInFirstOrLastPos,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase,
                 handle_one_type_not_first_pos: HandleOneTypeNotFirstPos):
        self.compl_type_in_first_or_second_pos: ComplTypeInFirstOrSecondPos = compl_type_in_first_or_second_pos
        self.compl_type_in_first_or_middle_pos: ComplTypeInFirstOrMiddlePos = compl_type_in_first_or_middle_pos
        self.compl_type_in_first_or_last_pos: ComplTypeInFirstOrLastPos = compl_type_in_first_or_last_pos
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.handle_one_type_not_first_pos: HandleOneTypeNotFirstPos = handle_one_type_not_first_pos

    def execute(self, voie : InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)

        if voie.has_type_in_first_pos:
            # 1er type + lib
            # test = VoieType('CHE DES SEMAPHORES', ['CHE', 'DES', 'SEMAPHORES'], ['CHEMIN'], [0], [])
            first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
            voie_traited = self.assign_type_lib_use_case.execute(voie, first_type)

        else:
            voie_traited = self.handle_one_type_not_first_pos.execute(voie)

        return voie_traited