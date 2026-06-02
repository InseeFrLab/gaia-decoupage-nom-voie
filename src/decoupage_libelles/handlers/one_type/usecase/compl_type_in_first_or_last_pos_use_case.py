from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_type_use_case import AssignLibTypeUseCase


class ComplTypeInFirstOrLastPosUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)

        if first_type.is_complement:
            self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=True)
            second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
            # Vérifier si le type de voie dans le libellé est écrit sous sa forme canonique
            if (second_type.type_name_in_lib == second_type.type_name and
                    not second_type.has_adj_det_before):
                # 'IMM SOLEIL RUE'
                # lib + 2eme type
                return self.assign_lib_type_use_case.execute(voie_compl, second_type)
            else:
                # 'IMM LE PARC'
                # lib
                return self.assign_lib_use_case.execute(voie_compl)

        elif second_type.is_complement:
            # 'IMP DU PAVILLON'
            # 1er type + lib
            return self.assign_type_lib_use_case.execute(voie_compl, first_type)
