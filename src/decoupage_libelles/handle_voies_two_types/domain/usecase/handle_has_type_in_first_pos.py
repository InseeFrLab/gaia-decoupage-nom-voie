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
    COMBINAISONS_LONG = {'CHEMIN/VOIE COMMUNALE': True,
                        'VOIE/RUE': False,
                        'IMPASSE/VOIE': True,
                        'IMPASSE/PLACE': False,
                        'CHEMIN/ALLEE': True,
                        'VOIE COMMUNALE/ROUTE': False,
                        'VOIE/VOIE COMMUNALE': True,
                        'VOIE COMMUNALE/CHEMIN': False,
                        'CHEMINEMENT/CHEMIN': False,
                        'CHEMIN/CHEMINEMENT': True,
                        'VOIE COMMUNALE/AVENUE': False,
                        'IMPASSE/ROUTE': False,
                        'VOIE COMMUNALE/BOULEVARD': False,
                        'IMPASSE/CHEMIN': False,
                        'RUE/ROUTE': True,
                        'ALLEE/VOIE COMMUNALE': True,
                        'ROUTE/VOIE COMMUNALE': True,
                        'PLACE/RUE': False,
                        'RUE/IMPASSE': True,
                        'RUE/VOIE COMMUNALE': True,
                        'RUE/CHEMIN': True,
                        'RUE/VOIE': True,
                        'ROUTE/RUE': False,
                        'IMPASSE/RUE': False,
                        'CHEMIN/ROUTE': False,
                        'IMPASSE/CHEMINEMENT': True,
                        'IMPASSE/BOULEVARD': False,
                        'AVENUE/VOIE COMMUNALE': True,
                        'RUE/AVENUE': False,
                        'VOIE COMMUNALE/IMPASSE': False,
                        'ALLEE/RUE': False,
                        'ROUTE/VOIE': True,
                        'AVENUE/IMPASSE': True,
                        'ROUTE/CHEMINEMENT': True,
                        'ROUTE/CHEMIN': True,
                        'PLACE/ROUTE': True,
                        'IMPASSE/AVENUE': False,
                        'CHEMINEMENT/VOIE COMMUNALE': True,
                        'RUE/ALLEE': True,
                        'RUE/CHEMINEMENT': True,
                        'CHEMIN/RUE': False,
                        'BOULEVARD/VOIE COMMUNALE': True,
                        'CHEMINEMENT/RUE': False,
                        'IMPASSE/VOIE COMMUNALE': True,
                        'RUE/PLACE': True,
                        'VOIE COMMUNALE/RUE': False,
                        'VOIE COMMUNALE/VOIE': False,
                        'VOIE COMMUNALE/CHEMINEMENT': False,
                        'VOIE COMMUNALE/ALLEE': False,
                        'CHEMINEMENT/VOIE': True,
                        'CHEMINEMENT/ROUTE': False,
                        'CHEMIN/AVENUE': False,
                        'CHEMIN/VOIE': True,
                        'CHEMIN/CHEMINEMENT': True,
                        'AVENUE/PLACE': True,
                        'AVENUE/CHEMINEMENT': True}

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
                        two_longs = ("/").join([first_type.type_name, second_type.type_name])
                        if first_type.type_name == second_type.type_name:
                            # lib
                            self.assign_lib_use_case.execute(voie)

                        elif (two_longs in HandleHasTypeInFirstPos.COMBINAISONS_LONG and
                                not HandleHasTypeInFirstPos.COMBINAISONS_LONG[two_longs]):
                            # compl + 2e type + lib
                            return self.assign_compl_type_lib_use_case.execute(voie, second_type)
                        else:
                            # 1er type + lib + compl
                            return self.assign_type_lib_compl_use_case.execute(voie)

                    elif (first_type.is_agglomerant and
                            second_type.is_agglomerant):
                        if first_type.type_name == second_type.type_name:
                            # lib
                            return self.assign_lib_use_case.execute(voie)
                        elif second_type.type_name == 'RESIDENCE':
                            # compl + 2e type + lib
                            return self.assign_compl_type_lib_use_case.execute(voie, second_type)
                        else:
                            # 1er type + lib + compl
                            return self.assign_type_lib_compl_use_case.execute(voie)

                    else:  # si le premier est long et le deuxieme agglo
                        # 1er type + lib + compl
                        return self.assign_type_lib_compl_use_case.execute(voie)