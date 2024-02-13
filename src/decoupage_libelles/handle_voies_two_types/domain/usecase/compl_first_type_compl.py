from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase


class ComplFirstTypeCompl:
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)

        if first_type.type_name in ComplementFinderUseCase.TYPES_COMPLEMENT_1_2:
            if second_type.is_longitudinal or second_type.is_agglomerant:
                # compl + 2e type + lib
                return self.assign_compl_type_lib_use_case.execute(voie_compl, second_type)
            elif third_type.is_longitudinal or third_type.is_agglomerant:
                # compl + 3e type + lib
                return self.assign_compl_type_lib_use_case.execute(voie_compl, third_type)
            else:
                # lib
                return self.assign_lib_use_case.execute(voie_compl)
