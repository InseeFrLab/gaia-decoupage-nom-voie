from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from handle_voies_two_types.domain.usecase.compl_immeuble_before_type import CompleImmeubleBeforeType
from handle_voies_two_types.domain.usecase.compl_two_types_long_or_agglo import ComplTwoTypesLongOrAgglo
from handle_voies_two_types.domain.usecase.compl_first_type_compl import ComplFirstTypeCompl
from handle_voies_two_types.domain.usecase.compl_second_type_compl import ComplSecondTypeCompl
from handle_voies_two_types.domain.usecase.compl_third_type_compl import ComplThirdTypeCompl


class HandleTwoTypesCompl():
    @inject
    def __init__(self,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 assign_lib_use_case: AssignLibUseCase,
                 compl_immeuble_before_type: CompleImmeubleBeforeType,
                 compl_two_types_long_or_agglo: ComplTwoTypesLongOrAgglo,
                 compl_first_type_compl: ComplFirstTypeCompl,
                 compl_second_type_compl: ComplSecondTypeCompl,
                 compl_third_type_compl: ComplThirdTypeCompl):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.compl_immeuble_before_type: CompleImmeubleBeforeType = compl_immeuble_before_type
        self.compl_two_types_long_or_agglo: ComplTwoTypesLongOrAgglo = compl_two_types_long_or_agglo
        self.compl_first_type_compl: ComplFirstTypeCompl = compl_first_type_compl
        self.compl_second_type_compl: ComplSecondTypeCompl = compl_second_type_compl
        self.compl_third_type_compl: ComplThirdTypeCompl = compl_third_type_compl

    def execute(self, voie_compl : InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

        voie_to_treat_by_compl, voie_to_treat_two_types = self.compl_immeuble_before_type.execute(voie_compl)

        if voie_to_treat_by_compl:
            voie_treated = self.compl_two_types_long_or_agglo.execute(voie_to_treat_by_compl)
            voie_treated = self.compl_first_type_compl.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.compl_second_type_compl.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.compl_third_type_compl.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.assign_lib_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated

        
        return voie_treated, voie_to_treat_two_types
