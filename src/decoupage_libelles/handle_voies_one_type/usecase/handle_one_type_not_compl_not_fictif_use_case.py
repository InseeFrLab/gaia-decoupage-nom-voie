from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_use_case import AssignTypeUseCase
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
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_type_use_case: AssignTypeUseCase = AssignTypeUseCase(),
        type_long_not_first_pos_use_case: TypeLongNotFirstPosUseCase = TypeLongNotFirstPosUseCase(),
        type_route_not_first_pos_use_case: TypeRouteNotFirstPosUseCase = TypeRouteNotFirstPosUseCase(),
        type_agglo_not_first_pos_use_case: TypeAggloNotFirstPosUseCase = TypeAggloNotFirstPosUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_type_use_case: AssignTypeUseCase = assign_type_use_case
        self.type_long_not_first_pos_use_case: TypeLongNotFirstPosUseCase = type_long_not_first_pos_use_case
        self.type_route_not_first_pos_use_case: TypeRouteNotFirstPosUseCase = type_route_not_first_pos_use_case
        self.type_agglo_not_first_pos_use_case: TypeAggloNotFirstPosUseCase = type_agglo_not_first_pos_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)
        voie_treated = None

        if voie.has_type_in_first_pos:
            first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
            if voie.has_type_in_last_pos:
                # 1 er type
                # "GRAND RUE"
                voie_treated = self.assign_type_use_case.execute(voie, first_type)
            else:
                # 1er type + lib
                # 'CHE DES SEMAPHORES'
                voie_treated = self.assign_type_lib_use_case.execute(voie, first_type)

        elif voie.has_type_in_last_pos:
            self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
            last_type = self.generate_information_on_type_ordered_use_case.execute(voie, -1)
            if (last_type.type_name == (' ').join(voie.label_preproc[last_type.position_start:last_type.position_end+1]) and
                not last_type.has_adj_det_before):
                voie_treated = self.assign_lib_type_use_case.execute(voie, last_type)

        if not voie_treated:
            voie_treated = self.type_long_not_first_pos_use_case.execute(voie)
            voie_treated = self.type_route_not_first_pos_use_case.execute(voie) if not voie_treated else voie_treated
            voie_treated = self.type_agglo_not_first_pos_use_case.execute(voie) if not voie_treated else voie_treated
            if not voie_treated:
                if voie.has_type_in_last_pos:
                    voie_treated = self.assign_lib_type_use_case.execute(voie)
                else:
                    voie_treated = self.assign_lib_use_case.execute(voie)

        return voie_treated
