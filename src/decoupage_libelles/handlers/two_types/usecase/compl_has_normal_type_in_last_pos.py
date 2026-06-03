from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupage_libelles.synonym_data.priorites_types import COMBINAISONS_LONG


class ComplHasNormalTypeInLastPos:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)

        if voie_compl.has_type_in_last_pos and not third_type.is_complement:
            first_type_not_compl = first_type if not first_type.is_complement else second_type
            last_type_not_compl = third_type
            two_longs = ("/").join([first_type_not_compl.type_name, last_type_not_compl.type_name])
            second_prio = two_longs in COMBINAISONS_LONG and not COMBINAISONS_LONG[two_longs]

            if not first_type_not_compl.is_longitudinal_or_agglomerant or second_prio:
                # VILLA PAVILLON AV
                return self.assign_lib_type_use_case.execute(voie_compl, last_type_not_compl)
