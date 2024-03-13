from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class TypeAggloNotFirstPosUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        if first_type.is_agglomerant:
            if not first_type.has_adj_det_before and voie.has_type_in_last_pos:
                # lib + 1er type
                # 'AVILLON HAM'
                return self.assign_lib_type_use_case.execute(voie)
            else:
                # lib
                # 'LE GRAND HAMEAU DE BIEVILLE'
                return self.assign_lib_use_case.execute(voie)
