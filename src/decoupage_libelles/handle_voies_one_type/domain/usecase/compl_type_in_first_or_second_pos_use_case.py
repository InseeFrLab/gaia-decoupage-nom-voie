from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase


class ComplTypeInFirstOrSecondPosUseCase:
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)

        if first_type.is_complement:
            if first_type.type_name in ComplementFinderUseCase.ORTHOGRAPHES_IMMEUBLE:
                if second_type.type_name in ComplementFinderUseCase.TYPES_COMPLEMENT_IMMEUBLE:
                    # 'IMM RESIDENCE BERYL'
                    # 2eme type + lib
                    return self.assign_type_lib_use_case.execute(voie_compl, second_type)
                else:
                    # "IMMEUBLE VAL D'ILLAZ"
                    # lib
                    return self.assign_lib_use_case.execute(voie_compl)

            else:
                # 'LDT VAL DES PINS'
                # lib
                return self.assign_lib_use_case.execute(voie_compl)
        
        elif second_type.is_complement:
            # 'VC  LDT LA PALUN CTE CENTRALE'
            # 1er type lib
            return self.assign_type_lib_use_case.execute(voie_compl, first_type)
