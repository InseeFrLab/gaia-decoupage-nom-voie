from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase


class HandleNoTypeInFirstPosUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
    ):
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
                # "LE CHATEAU LE GRAND HAMEAU"
                return self.assign_lib_use_case.execute(voie)

            else:
                if first_type.is_in_penultimate_position:
                    # lib
                    # "LA FONTAINE CHATEAU"
                    return self.assign_lib_use_case.execute(voie)
                else:
                    # compl + 1er type + lib
                    # "LA FONTAINE JUSSIEU HAMEAU" ??
                    return self.assign_compl_type_lib_use_case.execute(voie, first_type)

        else:
            if not first_type.is_longitudinal_or_agglomerant and not second_type.is_longitudinal_or_agglomerant:
                # lib
                # "LA FONTAINE DU CHATEAU VERDIN"
                return self.assign_lib_use_case.execute(voie)

            elif first_type.is_longitudinal_or_agglomerant and not second_type.is_longitudinal_or_agglomerant:
                if first_type.has_adj_det_before:
                    # lib
                    # "GRAND HAMEAU DE LA FONTAINE VERTE"
                    return self.assign_lib_use_case.execute(voie)
                else:
                    # compl + 1er type + lib
                    # "VERDIER RESIDENCE DE LA FONTAINE VERTE"
                    return self.assign_compl_type_lib_use_case.execute(voie, first_type)

            elif not first_type.is_longitudinal_or_agglomerant and second_type.is_longitudinal_or_agglomerant:
                # lib
                # "VERDIER FONTAINE DE LA RESIDENCE VERTE"
                return self.assign_lib_use_case.execute(voie)
            else:
                if first_type.has_adj_det_before or second_type.has_adj_det_before:
                    # lib
                    # "JUSSIEU RESIDENCE DE LA RUE HOCHE"
                    return self.assign_lib_use_case.execute(voie)

                else:
                    if first_type.is_longitudinal:
                        # compl + 1er type + lib
                        # "VERDIER RUE HOCHE RESIDENCE SOLEIL"
                        return self.assign_compl_type_lib_use_case.execute(voie, first_type)
                    elif first_type.is_agglomerant:  # équivalent à else
                        # compl + 2e type + lib
                        # "VERDIER RESIDENCE SOLEIL RUE HOCHE"
                        return self.assign_compl_type_lib_use_case.execute(voie, second_type)
