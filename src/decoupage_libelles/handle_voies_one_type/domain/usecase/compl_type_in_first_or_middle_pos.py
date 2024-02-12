from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from decoupe_voie.domain.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase


class ComplTypeInFirstOrMiddlePos:
    def __init__(self, generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_type_lib_compl_use_case: AssignTypeLibComplUseCase):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)

        if first_type.is_complement:
            if not second_type.has_adj_det_before:
                # 'BAT L ANJOU AVE DE VLAMINC'
                # compl + 2e type + lib
                voie_traited = self.assign_compl_type_lib_use_case.execute(voie_compl, second_type)
            else:
                # 'IMM LE LAC DU LOU'
                # lib
                voie_traited = self.assign_lib_use_case.execute(voie_compl)
        
        elif second_type.is_complement:
            if not second_type.has_adj_det_before:
                #  'HLM LES CHARTREUX BAT B2'
                # 1er type + lib + compl
                voie_traited = self.assign_type_lib_compl_use_case.execute(voie_compl, first_type, second_type)
            else:
                # 'RUE DU PAVILLON DE LA MARINE'
                # 1er type + lib
                voie_traited = self.assign_type_lib_use_case.execute(voie_compl, first_type)

        return voie_traited
