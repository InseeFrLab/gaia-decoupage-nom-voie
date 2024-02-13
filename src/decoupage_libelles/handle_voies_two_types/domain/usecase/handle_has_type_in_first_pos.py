from injector import inject

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase


class HandleHasTypeInFirstPos:
    @inject
    def __init__(self,
                 generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase,
                 generate_information_on_lib_use_case: GenerateInformationOnLibUseCase,
                 assign_type_lib_use_case: AssignTypeLibUseCase,
                 assign_compl_type_lib_use_case: AssignComplTypeLibUseCase,
                 assign_type_lib_compl_use_case: AssignTypeLibComplUseCase,
                 assign_lib_use_case: AssignLibUseCase):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

        if (voie.has_type_in_second_pos or
                voie.has_type_in_last_pos):
            # 1er type + lib
            return self.assign_type_lib_use_case.execute(voie, first_type)

        else:

            if (not first_type.is_longitudinal and not first_type.is_agglomerant and
                    not second_type.is_longitudinal and not second_type.is_agglomerant or
                    first_type.is_longitudinal and first_type.is_agglomerant and
                    not second_type.is_longitudinal and not second_type.is_agglomerant):
                # 1er type + lib
                return self.assign_type_lib_use_case.execute(voie, first_type)

            elif (not first_type.is_longitudinal and not first_type.is_agglomerant and
                    second_type.is_longitudinal and second_type.is_agglomerant):

                self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
                first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
                second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

                if second_type.has_adj_det_before:
                    # 1er type + lib
                    return self.assign_type_lib_use_case.execute(voie, first_type)
                else:
                    # compl + 2e type + lib
                    self.assign_compl_type_lib_use_case.execute(voie, second_type)

            else:
                self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)
                first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
                second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

                if second_type.has_adj_det_before:
                    # 1er type + lib
                    return self.assign_type_lib_use_case.execute(voie, first_type)

                else:
                    if (first_type.is_agglomerant and
                            second_type.is_longitudinal):
                        # compl + 2e type + lib
                        return self.assign_compl_type_lib_use_case.execute(voie, second_type)

                    elif (first_type.is_longitudinal and
                            second_type.is_longitudinal):
                        two_longs = ("/").join(voie.types_detected)
                        if voie.types_detected[0] == voie.types_detected[1]:
                            # lib
                            voie.assign_lib()

                        elif (two_longs in combinaisons_long and
                                not combinaisons_long[two_longs]):
                            # compl + 2e type + lib
                            return self.assign_compl_type_lib_use_case.execute(voie, second_type)
                        else:
                            # 1er type + lib + compl
                            return self.assign_type_lib_compl_use_case.execute(voie)

                    elif (first_type.is_agglomerant and
                            second_type.is_agglomerant):
                        if voie.types_detected[0] == voie.types_detected[1]:
                            # lib
                            return self.assign_lib_use_case.execute(voie)
                        elif voie.types_detected[1] in first_type_agglo:
                            # compl + 2e type + lib
                            return self.assign_compl_type_lib_use_case.execute(voie, second_type)
                        else:
                            # 1er type + lib + compl
                            return self.assign_type_lib_compl_use_case.execute(voie)

                    else:  # si le premier est long et le deuxieme agglo
                        # 1er type + lib + compl
                        return self.assign_type_lib_compl_use_case.execute(voie)