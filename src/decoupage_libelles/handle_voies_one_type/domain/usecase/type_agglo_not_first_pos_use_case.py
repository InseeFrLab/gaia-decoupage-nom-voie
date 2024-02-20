from injector import inject

from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from decoupe_voie.domain.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class TypeAggloNotFirstPosUseCase:
    @inject
    def __init__(self,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_lib_type_use_case: AssignLibTypeUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        if first_type.is_agglomerant:
            if (not first_type.has_adj_det_before and
                    voie.has_type_in_last_pos):
                # lib + 1er type
                # test = VoieType('AVILLON HAM', ['AVILLON', 'HAM'], ['HAMEAU'], [1], ['PROPN', 'PROPN'])
                return self.assign_lib_type_use_case.execute(voie)
            else:
                # lib
                # 'LE GRAND HAMEAU DE BIEVILLE'
                return self.assign_lib_use_case.execute(voie)
