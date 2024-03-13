from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class TypeRouteNotFirstPosUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        if first_type == "ROUTE":
            if first_type.word_before in ["C", "N", "D"] or first_type.word_after in ["C", "N", "D"]:
                # 1 er type + lib
                # 'N RTE NATIONALE 9'
                return self.assign_type_lib_use_case.execute(voie, first_type)
            else:
                # lib
                # 'LA ROUTE DES REVIERS'
                return self.assign_lib_use_case.execute(voie)
