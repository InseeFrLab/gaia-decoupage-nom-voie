from typing import List

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class DetectTypeFictifForMultiTypesUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        get_words_between_use_case: GetWordsBetweenUseCase = GetWordsBetweenUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.get_words_between_use_case: GetWordsBetweenUseCase = get_words_between_use_case

    def execute(self, voie: InfoVoie, liste_voie_commun: List[str], liste_fictive: List[str]) -> InfoVoie:
        for type_voie in liste_voie_commun:
            if type_voie in voie.types_detected:
                for occurence in range(1, 3):
                    if (type_voie, occurence) in voie.types_and_positions:
                        type_fictif: InformationOnTypeOrdered = self.generate_information_on_type_ordered_use_case.execute(voie, None, type_voie, occurence)
                        if type_fictif:
                            position_end = voie.types_and_positions[type_fictif.type_after][0] if type_fictif.type_after else None
                            elt_fictif = self.get_words_between_use_case.execute(voie, type_fictif.position_start + 1, position_end)
                            if elt_fictif:
                                elt_fictif = elt_fictif.split(" ")
                                one_word_label_fictif = True if len(elt_fictif) == 1 else False
                                has_type_fictif_in_last_pos = True if not type_fictif.type_after else False
                                if one_word_label_fictif and elt_fictif[0] in liste_fictive or one_word_label_fictif and elt_fictif[0] in ["L", "D"] and has_type_fictif_in_last_pos:
                                    return voie
        return None
