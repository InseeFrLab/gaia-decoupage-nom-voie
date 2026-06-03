from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_use_case import AssignLibUseCase


class ComplFirstTypeComplUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)

        if first_type.is_complement:
            if voie_compl.has_type_in_first_pos and voie_compl.has_type_in_second_pos:
                # 'BAT VAL DES PINS'
                # lib
                return self.assign_lib_use_case.execute(voie_compl)

            elif second_type.is_longitudinal_or_agglomerant:
                # compl + 2e type + lib
                # "PAVILLON BEAU SOLEIL LOT DE LA FONTAINE"
                return self.assign_compl_type_lib_use_case.execute(voie_compl, second_type)
            elif third_type.is_longitudinal_or_agglomerant:
                # compl + 3e type + lib
                # "PAVILLON LA FONTAINE LOT BEAU SOLEIL"
                return self.assign_compl_type_lib_use_case.execute(voie_compl, third_type)
            else:
                # lib
                # "PAVILLON LA FONTAINE CHATEAU BEAU SOLEIL"
                return self.assign_lib_use_case.execute(voie_compl)
