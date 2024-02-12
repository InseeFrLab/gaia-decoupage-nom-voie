from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase

class TypeRouteNotFirstPos:
    @inject
    def __init__(self,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        if first_type == 'ROUTE':
            if (first_type.word_before in ['C', 'N', 'D'] or
                    first_type.word_after in ['C', 'N', 'D']):
                # 1 er type + lib
                # test = VoieType('N RTE NATIONALE 9', ['N', 'RTE', 'NATIONALE', '9'], ['ROUTE'], [1], ['PRON', 'PRON', 'ADJ', 'NUM'])
                return self.assign_type_lib_use_case.execute(voie, first_type)
            else:
                # lib
                # 'LA ROUTE DES REVIERS'
                return self.assign_lib_use_case.execute(voie)
