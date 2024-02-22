from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase


class HandleNoTypeComplUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_lib_compl_use_case: AssignLibComplUseCase = AssignLibComplUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_compl_use_case: AssignLibComplUseCase = assign_lib_compl_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)

        if first_type.is_in_middle_position and not first_type.has_adj_det_before:
            # 'LE TILLET BAT A'
            # lib + compl
            return self.assign_lib_compl_use_case.execute(voie_compl)

        else:
            # 'BAT JEAN LAMOUR'
            # lib
            return self.assign_lib_use_case.execute(voie_compl)
