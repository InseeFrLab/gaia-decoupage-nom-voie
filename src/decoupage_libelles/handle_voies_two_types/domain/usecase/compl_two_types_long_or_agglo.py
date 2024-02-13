from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_compl_use_case import AssignComplTypeLibComplUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase


class ComplTwoTypesLongOrAgglo:
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_compl_type_lib_compl_use_case: AssignComplTypeLibComplUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_type_lib_compl_use_case: AssignTypeLibComplUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_compl_use_case: AssignComplTypeLibComplUseCase = assign_compl_type_lib_compl_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)


        if (first_type.is_agglomerant and
                second_type.is_longitudinal):
            # 'HLM AVE KLEBER BAT DESCARTES'
            # compl + 2e type + lib + 3e type compl
            return self.assign_compl_type_lib_compl_use_case.execute(voie_compl, second_type, third_type)

        elif (first_type.is_agglomerant and
                third_type.is_longitudinal or
                second_type.is_agglomerant and
                third_type.is_longitudinal):
            # compl + 3e type + lib
            return self.assign_compl_type_lib_use_case.execute(voie_compl, third_type)

        elif (first_type.is_longitudinal and
                second_type.is_agglomerant or
                first_type.is_longitudinal and
                third_type.is_agglomerant):
            # 1er type + lib + 2e type compl
            return self.assign_type_lib_compl_use_case.execute(voie_compl)

        else:
            # IMM BLEU RUE DES LYS RESIDENCE ERNEST RENAN
            # compl + 2e type + lib + 3e compl
            return self.assign_compl_type_lib_compl_use_case.execute(voie_compl, second_type, third_type)
