from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.handle_voies_two_types.usecase.compl_immeuble_before_type_use_case import ComplImmeubleBeforeTypeUseCase
from decoupage_libelles.handle_voies_two_types.usecase.compl_two_types_long_or_agglo_use_case import ComplTwoTypesLongOrAggloUseCase
from decoupage_libelles.handle_voies_two_types.usecase.compl_first_type_compl_use_case import ComplFirstTypeComplUseCase
from decoupage_libelles.handle_voies_two_types.usecase.compl_second_type_compl_use_case import ComplSecondTypeComplUseCase
from decoupage_libelles.handle_voies_two_types.usecase.compl_third_type_compl_use_case import ComplThirdTypeComplUseCase


class HandleTwoTypesComplUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        compl_immeuble_before_type_use_case: ComplImmeubleBeforeTypeUseCase = ComplImmeubleBeforeTypeUseCase(),
        compl_two_types_long_or_agglo_use_case: ComplTwoTypesLongOrAggloUseCase = ComplTwoTypesLongOrAggloUseCase(),
        compl_first_type_compl_use_case: ComplFirstTypeComplUseCase = ComplFirstTypeComplUseCase(),
        compl_second_type_compl_use_case: ComplSecondTypeComplUseCase = ComplSecondTypeComplUseCase(),
        compl_third_type_compl_use_case: ComplThirdTypeComplUseCase = ComplThirdTypeComplUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.compl_immeuble_before_type_use_case: ComplImmeubleBeforeTypeUseCase = compl_immeuble_before_type_use_case
        self.compl_two_types_long_or_agglo_use_case: ComplTwoTypesLongOrAggloUseCase = compl_two_types_long_or_agglo_use_case
        self.compl_first_type_compl_use_case: ComplFirstTypeComplUseCase = compl_first_type_compl_use_case
        self.compl_second_type_compl_use_case: ComplSecondTypeComplUseCase = compl_second_type_compl_use_case
        self.compl_third_type_compl_use_case: ComplThirdTypeComplUseCase = compl_third_type_compl_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

        # voie_to_treat_by_compl, voie_to_treat_two_types = self.compl_immeuble_before_type_use_case.execute(voie_compl)

        voie_to_treat_by_compl = voie_compl
        voie_to_treat_two_types = None

        voie_treated = None
        if voie_to_treat_by_compl:
            voie_treated = self.compl_two_types_long_or_agglo_use_case.execute(voie_to_treat_by_compl)
            voie_treated = self.compl_first_type_compl_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.compl_second_type_compl_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.compl_third_type_compl_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated
            voie_treated = self.assign_lib_use_case.execute(voie_to_treat_by_compl) if not voie_treated else voie_treated

        return voie_treated, voie_to_treat_two_types
