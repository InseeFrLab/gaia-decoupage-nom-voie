from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_type_lib_use_case import AssignTypeLibUseCase


class ComplTypeInFirstOrSecondPosUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)

        if first_type.is_complement:
            # 'IMM RESIDENCE BERYL'
            # compl + 2eme type + lib
            return self.assign_compl_type_lib_use_case.execute(voie_compl, second_type)

        elif second_type.is_complement:
            # 'VC  PAVILLON LA PALUN CTE CENTRALE'
            # 1er type + lib
            return self.assign_type_lib_use_case.execute(voie_compl, first_type)
