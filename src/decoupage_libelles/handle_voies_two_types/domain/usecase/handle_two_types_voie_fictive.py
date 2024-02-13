from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase


class HandleTwoTypesVoieFictive:
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_type_lib_compl_use_case: AssignTypeLibComplUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

        if second_type.position_start - first_type.position_end > 2:
            # 1er type + lib + compl
            return self.assign_type_lib_compl_use_case.execute(voie)
        else:
            words_between_types = voie.label_preproc[first_type.position_end + 1: second_type.position_start]
            if len(words_between_types) == 1:
                # compl + 2e type + lib
                return self.assign_compl_type_lib_use_case.execute(voie, second_type)
            else:
                # 1er type + lib + compl
                return self.assign_type_lib_compl_use_case.execute(voie)