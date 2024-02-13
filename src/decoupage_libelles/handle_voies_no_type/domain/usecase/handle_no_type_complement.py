from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase


class HandleNoTypeCompl():
    def __init__(self, generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_lib_compl_use_case: AssignLibComplUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_compl_use_case: AssignLibComplUseCase = assign_lib_compl_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)

        if (first_type.is_in_middle_position and not
                first_type.has_adj_det_before):
            # 'LE TILLET BAT A'
            # lib + compl
            return self.assign_lib_compl_use_case.execute(voie_compl)

        else:
            # 'BAT JEAN LAMOUR'
            # lib
            return self.assign_lib_use_case.execute(voie_compl)
