from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase

class TypeLongNotFirstPos:   
    @inject
    def __init__(self,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        if first_type.is_longitudinal:
            if (not first_type.has_adj_det_before and
                not voie.has_type_in_last_pos):
                # compl + 1er type + lib
                # test = VoieType('LE BAS FAURE RUE DE TOUL', ['LE', 'BAS', 'FAURE', 'RUE', 'DE', 'TOUL'], ['RUE'], [3], ['DET', 'PROPN', 'PROPN', 'NOUN', 'ADP', 'PROPN'])
                return self.assign_compl_type_lib_use_case.execute(voie, first_type)
            else:
                # lib
                # 'LA BELLE AVENUE'
                return self.assign_lib_use_case.execute(voie)