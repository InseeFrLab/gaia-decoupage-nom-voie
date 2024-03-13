from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase


class ComplThirdTypeComplUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = AssignTypeLibComplUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)

        if third_type.type_name in ComplementFinderUseCase.TYPES_COMPLEMENT_1_2:
            if first_type.is_longitudinal or first_type.is_agglomerant:
                # 1er type + lib + 3e type compl
                return self.assign_type_lib_compl_use_case.execute(voie_compl, first_type, third_type)
            elif second_type.is_longitudinal or second_type.is_agglomerant:
                # lib
                return self.assign_lib_use_case.execute(voie_compl)
            else:
                # lib
                return self.assign_lib_use_case.execute(voie_compl)
