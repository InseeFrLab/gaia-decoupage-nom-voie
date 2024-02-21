from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from handle_voies_two_types.domain.usecase.compl_immeuble_before_type_use_case import ComplImmeubleBeforeTypeUseCase
from handle_voies_two_types.domain.usecase.compl_two_types_long_or_agglo_use_case import ComplTwoTypesLongOrAggloUseCase
from handle_voies_two_types.domain.usecase.compl_first_type_compl_use_case import ComplFirstTypeComplUseCase
from handle_voies_two_types.domain.usecase.compl_second_type_compl_use_case import ComplSecondTypeComplUseCase
from handle_voies_two_types.domain.usecase.compl_third_type_compl_use_case import ComplThirdTypeComplUseCase


class HandleTwoTypesComplUseCase:
    @inject
    def __init__(self,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 assign_lib_use_case: AssignLibUseCase,
                 compl_immeuble_before_type_use_case: ComplImmeubleBeforeTypeUseCase,
                 compl_two_types_long_or_agglo_use_case: ComplTwoTypesLongOrAggloUseCase,
                 compl_first_type_compl_use_case: ComplFirstTypeComplUseCase,
                 compl_second_type_compl_use_case: ComplSecondTypeComplUseCase,
                 compl_third_type_compl_use_case: ComplThirdTypeComplUseCase):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.compl_immeuble_before_type_use_case: ComplImmeubleBeforeTypeUseCase = compl_immeuble_before_type_use_case
        self.compl_two_types_long_or_agglo_use_case: ComplTwoTypesLongOrAggloUseCase = compl_two_types_long_or_agglo_use_case
        self.compl_first_type_compl_use_case: ComplFirstTypeComplUseCase = compl_first_type_compl_use_case
        self.compl_second_type_compl_use_case: ComplSecondTypeComplUseCase = compl_second_type_compl_use_case
        self.compl_third_type_compl_use_case: ComplThirdTypeComplUseCase = compl_third_type_compl_use_case

    def execute(self, voie_compl : InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

        voie_to_treat_by_compl, voie_to_treat_two_types = self.compl_immeuble_before_type_use_case.execute(voie_compl)

        if voie_to_treat_by_compl:
            voie_treated = self.compl_two_types_long_or_agglo_use_case.execute(voie_to_treat_by_compl)
            voie_treated = self.compl_first_type_compl_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.compl_second_type_compl_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.compl_third_type_compl_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.assign_lib_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated

        
        return voie_treated, voie_to_treat_two_types
