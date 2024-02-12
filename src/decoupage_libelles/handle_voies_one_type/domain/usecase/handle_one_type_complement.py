from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_second_pos import ComplTypeInFirstOrSecondPos
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_middle_pos import ComplTypeInFirstOrMiddlePos
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_last_pos import ComplTypeInFirstOrLastPos


class HandleOneTypeCompl():
    @inject
    def __init__(self, compl_type_in_first_or_second_pos: ComplTypeInFirstOrSecondPos,
                 compl_type_in_first_or_middle_pos: ComplTypeInFirstOrMiddlePos,
                 compl_type_in_first_or_last_pos: ComplTypeInFirstOrLastPos,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.compl_type_in_first_or_second_pos: ComplTypeInFirstOrSecondPos = compl_type_in_first_or_second_pos
        self.compl_type_in_first_or_middle_pos: ComplTypeInFirstOrMiddlePos = compl_type_in_first_or_middle_pos
        self.compl_type_in_first_or_last_pos: ComplTypeInFirstOrLastPos = compl_type_in_first_or_last_pos
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie_compl : InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

        if voie_compl.has_type_in_first_pos:

            if voie_compl.has_type_in_second_pos:
                voie_traited = self.compl_type_in_first_or_second_pos.execute(voie_compl)

            elif voie_compl.has_type_in_last_pos:
                voie_traited = self.compl_type_in_first_or_last_pos.execute(voie_compl)

            else:
                voie_traited = self.compl_type_in_first_or_middle_pos.execute(voie_compl)

        else:
            # 'LE PAVILLON DE LA FORET'
            # lib
            voie_traited = self.assign_lib_use_case.execute(voie_compl)
        
        return voie_traited
