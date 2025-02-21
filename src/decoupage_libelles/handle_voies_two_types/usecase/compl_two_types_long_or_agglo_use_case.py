from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_compl_use_case import AssignComplTypeLibComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase


class ComplTwoTypesLongOrAggloUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_compl_type_lib_compl_use_case: AssignComplTypeLibComplUseCase = AssignComplTypeLibComplUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = AssignTypeLibComplUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_compl_use_case: AssignComplTypeLibComplUseCase = assign_compl_type_lib_compl_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)

        if first_type.is_agglomerant and second_type.is_longitudinal:
            # 'HLM AV KLEBER BAT DESCARTES'
            # compl + 2e type + lib + 3e type compl
            return self.assign_compl_type_lib_compl_use_case.execute(voie_compl, second_type, third_type)

        elif first_type.is_agglomerant and third_type.is_longitudinal or second_type.is_agglomerant and third_type.is_longitudinal:
            # "HLM BAT DESCARTES AV KLEBER"
            # compl + 3e type + lib
            return self.assign_compl_type_lib_use_case.execute(voie_compl, third_type)

        elif first_type.is_longitudinal and second_type.is_agglomerant or first_type.is_longitudinal and third_type.is_agglomerant:
            # 1er type + lib + 2e type compl
            # "RUE HOCHE HLM BAT DESCARTES"
            return self.assign_type_lib_compl_use_case.execute(voie_compl)

        elif second_type.is_agglomerant and third_type.is_agglomerant or second_type.is_longitudinal and third_type.is_longitudinal or second_type.is_longitudinal and third_type.is_agglomerant:
            # "IMM BLEU RUE DES LYS RESIDENCE ERNEST RENAN"
            # compl + 2e type + lib + 3e compl
            return self.assign_compl_type_lib_compl_use_case.execute(voie_compl, second_type, third_type)
