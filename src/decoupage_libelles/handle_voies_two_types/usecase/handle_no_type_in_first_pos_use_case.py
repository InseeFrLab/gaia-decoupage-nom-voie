from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_compl_use_case import AssignComplTypeLibComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase


class HandleNoTypeInFirstPosUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_compl_type_lib_compl_use_case: AssignComplTypeLibComplUseCase = AssignComplTypeLibComplUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_compl_type_lib_compl_use_case: AssignComplTypeLibComplUseCase = assign_compl_type_lib_compl_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie, 2)

        if voie.has_type_in_last_pos:
            last_type = self.generate_information_on_type_ordered_use_case.execute(voie, -1)
            last_type_name_in_lib = (' ').join(voie.label_preproc[last_type.position_start:last_type.position_end+1])
            if last_type.type_name == last_type_name_in_lib:
                return self.assign_lib_type_use_case.execute(voie, last_type)
            else:
                return self.assign_lib_use_case.execute(voie)

        else:
            if not first_type.is_longitudinal_or_agglomerant and not second_type.is_longitudinal_or_agglomerant:
                # lib
                # "LA FONTAINE DU CHATEAU VERDIN"
                return self.assign_lib_use_case.execute(voie)

            elif first_type.is_longitudinal_or_agglomerant and not second_type.is_longitudinal_or_agglomerant:
                # compl + 1er type + lib
                # "VERDIER RESIDENCE DE LA FONTAINE VERTE"
                return self.assign_compl_type_lib_use_case.execute(voie, first_type)

            elif not first_type.is_longitudinal_or_agglomerant and second_type.is_longitudinal_or_agglomerant:
                # lib
                # "VERDIER FONTAINE DE LA RESIDENCE VERTE"
                return self.assign_lib_use_case.execute(voie)
            else:
                if first_type.is_longitudinal:
                    # compl + 1er type + lib + compl
                    # "VERDIER RUE HOCHE RESIDENCE SOLEIL"
                    return self.assign_compl_type_lib_compl_use_case.execute(voie, first_type, second_type)
                elif first_type.is_agglomerant:  # équivalent à else
                    # compl + 2e type + lib
                    # "VERDIER RESIDENCE SOLEIL RUE HOCHE"
                    return self.assign_compl_type_lib_use_case.execute(voie, second_type)
