from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase


class HandleHasTypeInFirstPosUseCase:
    COMBINAISONS_LONG = {
        "CHEMIN/VOIE COMMUNALE": True,
        "VOIE/RUE": False,
        "IMPASSE/VOIE": True,
        "IMPASSE/PLACE": False,
        "CHEMIN/ALLEE": True,
        "VOIE COMMUNALE/ROUTE": False,
        "VOIE/VOIE COMMUNALE": True,
        "VOIE COMMUNALE/CHEMIN": False,
        "CHEMINEMENT/CHEMIN": False,
        "CHEMIN/CHEMINEMENT": True,
        "VOIE COMMUNALE/AVENUE": False,
        "IMPASSE/ROUTE": False,
        "VOIE COMMUNALE/BOULEVARD": False,
        "IMPASSE/CHEMIN": False,
        "RUE/ROUTE": True,
        "ALLEE/VOIE COMMUNALE": True,
        "ROUTE/VOIE COMMUNALE": True,
        "PLACE/RUE": False,
        "RUE/IMPASSE": True,
        "RUE/VOIE COMMUNALE": True,
        "RUE/CHEMIN": True,
        "RUE/VOIE": True,
        "ROUTE/RUE": False,
        "IMPASSE/RUE": False,
        "CHEMIN/ROUTE": False,
        "IMPASSE/CHEMINEMENT": True,
        "IMPASSE/BOULEVARD": False,
        "AVENUE/VOIE COMMUNALE": True,
        "RUE/AVENUE": False,
        "VOIE COMMUNALE/IMPASSE": False,
        "ALLEE/RUE": False,
        "ROUTE/VOIE": True,
        "AVENUE/IMPASSE": True,
        "ROUTE/CHEMINEMENT": True,
        "ROUTE/CHEMIN": True,
        "PLACE/ROUTE": True,
        "IMPASSE/AVENUE": False,
        "CHEMINEMENT/VOIE COMMUNALE": True,
        "RUE/ALLEE": True,
        "RUE/CHEMINEMENT": True,
        "CHEMIN/RUE": False,
        "BOULEVARD/VOIE COMMUNALE": True,
        "CHEMINEMENT/RUE": False,
        "IMPASSE/VOIE COMMUNALE": True,
        "RUE/PLACE": True,
        "VOIE COMMUNALE/RUE": False,
        "VOIE COMMUNALE/VOIE": False,
        "VOIE COMMUNALE/CHEMINEMENT": False,
        "VOIE COMMUNALE/ALLEE": False,
        "CHEMINEMENT/VOIE": True,
        "CHEMINEMENT/ROUTE": False,
        "CHEMIN/AVENUE": False,
        "CHEMIN/VOIE": True,
        "CHEMIN/CHEMINEMENT": True,
        "AVENUE/PLACE": True,
        "AVENUE/CHEMINEMENT": True,
    }

    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = AssignTypeLibComplUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

        if voie.has_type_in_second_pos or voie.has_type_in_last_pos:
            second_type_name_in_lib = (' ').join(voie.label_preproc[second_type.position_start:second_type.position_end+1])
            if (voie.has_type_in_last_pos and
                    second_type.type_name == second_type_name_in_lib):
                two_longs = ("/").join([first_type.type_name, second_type.type_name])
                last_type_prio = two_longs in HandleHasTypeInFirstPosUseCase.COMBINAISONS_LONG and not HandleHasTypeInFirstPosUseCase.COMBINAISONS_LONG[two_longs]
                first_type_name_in_lib = (' ').join(voie.label_preproc[first_type.position_start:first_type.position_end+1])
                if (first_type.type_name != first_type_name_in_lib or
                        not first_type.is_longitudinal_or_agglomerant or
                        last_type_prio):
                    last_type = self.generate_information_on_type_ordered_use_case.execute(voie, -1)
                    return self.assign_lib_type_use_case.execute(voie, last_type)
                else:
                    # 1er type + lib
                    return self.assign_type_lib_use_case.execute(voie, first_type)
            else:
                # 1er type + lib
                # "RUE RESIDENCE SOLEIL"
                return self.assign_type_lib_use_case.execute(voie, first_type)

        else:
            if not second_type.is_longitudinal_or_agglomerant:
                # 1er type + lib
                # "FONTAINE DU CHATEAU"
                # "RUE DU CHATEAU"
                return self.assign_type_lib_use_case.execute(voie, first_type)

            elif not first_type.is_longitudinal_or_agglomerant and second_type.is_longitudinal_or_agglomerant:
                # compl + 2e type + lib
                # "CHATEAU DE VERSAILLES RUE HOCHE"
                return self.assign_compl_type_lib_use_case.execute(voie, second_type)

            else:
                if first_type.is_agglomerant and second_type.is_longitudinal:
                    # compl + 2e type + lib
                    # "RESIDENCE VINCENNES RUE HOCHE"
                    return self.assign_compl_type_lib_use_case.execute(voie, second_type)

                elif first_type.is_longitudinal and second_type.is_longitudinal:
                    two_longs = ("/").join([first_type.type_name, second_type.type_name])
                    if first_type.type_name == second_type.type_name:
                        # lib
                        # "RUE HOCHE RUE VERDIER"
                        return self.assign_lib_use_case.execute(voie)

                    elif two_longs in HandleHasTypeInFirstPosUseCase.COMBINAISONS_LONG and not HandleHasTypeInFirstPosUseCase.COMBINAISONS_LONG[two_longs]:
                        # compl + 2e type + lib
                        # "IMPASSE HOCHE AVENUE VERDIER"
                        return self.assign_compl_type_lib_use_case.execute(voie, second_type)
                    else:
                        # 1er type + lib + compl
                        # "AVENUE VERDIER IMPASSE HOCHE"
                        return self.assign_type_lib_compl_use_case.execute(voie)

                elif first_type.is_agglomerant and second_type.is_agglomerant:
                    if first_type.type_name == second_type.type_name:
                        # lib
                        # "HAMEAU SOLEIL HAMEAU VERDIER"
                        return self.assign_lib_use_case.execute(voie)
                    elif second_type.type_name in ["RESIDENCE", "HLM"]:
                        # compl + 2e type + lib
                        # "HAMEAU SOLEIL RESIDENCE BLEUE"
                        return self.assign_type_lib_compl_use_case.execute(voie, second_type, first_type)
                    else:
                        # 1er type + lib + compl
                        # "HAMEAU SOLEIL LOTISSEMENT VERDIER"
                        return self.assign_type_lib_compl_use_case.execute(voie)

                else:  # si le premier est long et le deuxieme agglo
                    # 1er type + lib + compl
                    # "RUE HOCHE RESIDENCE ERNEST RENAN"
                    return self.assign_type_lib_compl_use_case.execute(voie)
