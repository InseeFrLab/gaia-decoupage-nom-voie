from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class TypeLongNotFirstPosUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase()
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_lib_type_use_case : AssignLibTypeUseCase = assign_lib_type_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        if first_type.is_longitudinal:
            if not first_type.has_adj_det_before and not voie.has_type_in_last_pos:
                # compl + 1er type + lib
                # 'LE BAS FAURE RUE DE TOUL'
                return self.assign_compl_type_lib_use_case.execute(voie, first_type)
            elif not first_type.has_adj_det_before and voie.has_type_in_last_pos:
                # lib + 1er type
                # 'HOCHE RUE'
                return self.assign_lib_type_use_case.execute(voie)
            else:
                # lib
                # 'LA BELLE AVENUE'
                return self.assign_lib_use_case.execute(voie)
