from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.handle_voies_one_type.usecase.type_long_not_first_pos_use_case import TypeLongNotFirstPosUseCase
from decoupage_libelles.handle_voies_one_type.usecase.type_route_not_first_pos_use_case import TypeRouteNotFirstPosUseCase
from decoupage_libelles.handle_voies_one_type.usecase.type_agglo_not_first_pos_use_case import TypeAggloNotFirstPosUseCase


class HandleOneTypeNotComplNotFictifUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        type_long_not_first_pos_use_case: TypeLongNotFirstPosUseCase = TypeLongNotFirstPosUseCase(),
        type_route_not_first_pos_use_case: TypeRouteNotFirstPosUseCase = TypeRouteNotFirstPosUseCase(),
        type_agglo_not_first_pos_use_case: TypeAggloNotFirstPosUseCase = TypeAggloNotFirstPosUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.type_long_not_first_pos_use_case: TypeLongNotFirstPosUseCase = type_long_not_first_pos_use_case
        self.type_route_not_first_pos_use_case: TypeRouteNotFirstPosUseCase = type_route_not_first_pos_use_case
        self.type_agglo_not_first_pos_use_case: TypeAggloNotFirstPosUseCase = type_agglo_not_first_pos_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)

        if voie.has_type_in_first_pos:
            # 1er type + lib
            # test = VoieType('CHE DES SEMAPHORES', ['CHE', 'DES', 'SEMAPHORES'], ['CHEMIN'], [0], [])
            first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
            voie_treated = self.assign_type_lib_use_case.execute(voie, first_type)

        else:
            voie_treated = self.type_long_not_first_pos_use_case.execute(voie)
            voie_treated = self.type_route_not_first_pos_use_case.execute(voie) if not voie_treated else voie_treated
            voie_treated = self.type_agglo_not_first_pos_use_case.execute(voie) if not voie_treated else voie_treated
            voie_treated = self.assign_lib_use_case.execute(voie) if not voie_treated else voie_treated

        return voie_treated
