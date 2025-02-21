from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase


class ComplTypeInFirstOrLastPosUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)

        if first_type.is_complement:
            if first_type.is_escalier_or_appartement:
                # 'APPARTEMENT LE PARC'
                # lib
                return self.assign_lib_use_case.execute(voie_compl)
            else:
                # 'IMM LE PARC'
                # 1er type + lib
                return self.assign_type_lib_use_case.execute(voie_compl, first_type)

        elif second_type.is_complement:
            # 'IMP DU PAVILLON'
            # 1er type + lib
            return self.assign_type_lib_use_case.execute(voie_compl, first_type)
