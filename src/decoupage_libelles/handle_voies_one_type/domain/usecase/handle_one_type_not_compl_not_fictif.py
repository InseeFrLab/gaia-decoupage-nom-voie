from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from handle_voies_one_type.domain.usecase.type_long_not_first_pos import TypeLongNotFirstPos
from handle_voies_one_type.domain.usecase.type_route_not_first_pos import TypeRouteNotFirstPos
from handle_voies_one_type.domain.usecase.type_agglo_not_first_pos import TypeAggloNotFirstPos


class HandleOneTypeNotComplNotFictif:
    @inject
    def __init__(self,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase,
                 type_long_not_first_pos: TypeLongNotFirstPos,
                 type_route_not_first_pos: TypeRouteNotFirstPos,
                 type_agglo_not_first_pos: TypeAggloNotFirstPos):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.type_long_not_first_pos: TypeLongNotFirstPos = type_long_not_first_pos
        self.type_route_not_first_pos: TypeRouteNotFirstPos = type_route_not_first_pos
        self.type_agglo_not_first_pos: TypeAggloNotFirstPos = type_agglo_not_first_pos


    def execute(self, voie : InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)

        if voie.has_type_in_first_pos:
            # 1er type + lib
            # test = VoieType('CHE DES SEMAPHORES', ['CHE', 'DES', 'SEMAPHORES'], ['CHEMIN'], [0], [])
            first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
            voie_treated = self.assign_type_lib_use_case.execute(voie, first_type)

        else:
            voie_treated = self.type_long_not_first_pos.execute(voie)
            voie_treated = self.type_route_not_first_pos.execute(voie) if not voie_treated else voie_treated
            voie_treated = self.type_agglo_not_first_pos.execute(voie) if not voie_treated else voie_treated
            voie_treated = self.assign_lib_use_case.execute(voie) if not voie_treated else voie_treated

        return voie_treated