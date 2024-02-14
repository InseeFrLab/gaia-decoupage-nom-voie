from injector import inject

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase


class HandleNoTypeInFirstPos:
    @inject
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

        if voie.has_type_in_last_pos:
            if second_type.has_adj_det_before:
                # lib
                return self.assign_lib_use_case.execute(voie)

            else:
                if first_type.is_in_penultimate_position:
                    # lib
                    return self.assign_lib_use_case.execute(voie)
                else:
                    # compl + 1er type + lib
                    return self.assign_compl_type_lib_use_case.execute(voie, first_type)

        else:
            if (not first_type.is_longitudinal and not first_type.is_agglomerant and
                    not second_type.is_longitudinal and not second_type.is_agglomerant):
                # lib
                return self.assign_lib_use_case.execute(voie)

            elif (first_type.is_longitudinal and first_type.is_agglomerant and
                    not second_type.is_longitudinal and not second_type.is_agglomerant):
                if first_type.has_adj_det_before:
                    # lib
                    return self.assign_lib_use_case.execute(voie)
                else:
                    # compl + 1er type + lib
                    return self.assign_compl_type_lib_use_case.execute(voie, first_type)

            elif (not first_type.is_longitudinal and not first_type.is_agglomerant and
                    second_type.is_longitudinal and second_type.is_agglomerant):
                # lib
                return self.assign_lib_use_case.execute(voie)
            else:
                if first_type.has_adj_det_before:
                    # lib
                    return self.assign_lib_use_case.execute(voie)

                else:
                    if first_type.is_longitudinal:
                        # compl + 1er type + lib
                        return self.assign_compl_type_lib_use_case.execute(voie, first_type)
                    elif first_type.is_agglomerant:  # équivalent à else
                        # compl + 2e type + lib
                        return self.assign_compl_type_lib_use_case.execute(voie, second_type)