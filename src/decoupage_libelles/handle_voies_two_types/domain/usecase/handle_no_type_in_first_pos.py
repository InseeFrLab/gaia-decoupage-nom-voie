from injector import inject

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase


class HandleNoTypeInFirstPos:
    @inject
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        if voie.has_type_in_last_pos:
            if voie.has_adj_det_before_type(1):
                # lib
                voie.assign_lib()

            else:
                if voie.has_type_in_penultimate_pos(0):
                    # lib
                    voie.assign_lib()
                else:
                    # compl + 1er type + lib
                    voie.assign_compl_type_lib(0)

        else:
            if (not voie.type_is_long_or_agglo(0) and
                    not voie.type_is_long_or_agglo(1)):
                # lib
                voie.assign_lib()

            elif (voie.type_is_long_or_agglo(0) and
                    not voie.type_is_long_or_agglo(1)):
                if voie.has_adj_det_before_type(0):
                    # lib
                    voie.assign_lib()
                else:
                    # compl + 1er type + lib
                    voie.assign_compl_type_lib(0)

            elif (not voie.type_is_long_or_agglo(0) and
                    voie.type_is_long_or_agglo(1)):
                # lib
                voie.assign_lib()
            else:
                if voie.has_adj_det_before_type(0):
                    # lib
                    voie.assign_lib()

                else:
                    if voie.type_is_long(0):
                        # compl + 1er type + lib
                        voie.assign_compl_type_lib(0)
                    elif voie.type_is_agglo(0):  # équivalent à else
                        # compl + 2e type + lib
                        voie.assign_compl_type_lib(1)