from typing import List, Optional

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class DetectTypeFictifForOneTypeUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case

    def execute(self, voie: InfoVoie, liste_voie_commun: List[str], liste_fictive: List[str]) -> Optional[InfoVoie]:
        # si RUE A on garde type 'RUE' et libellé 'A'. Si il y a qlq chose avant 'RUE',
        # alors ca passe en voie fictive

        for type_voie in liste_voie_commun:
            first_type: InformationOnTypeOrdered = self.generate_information_on_type_ordered_use_case.execute(voie, 1)

            if first_type.type_name == type_voie and first_type.is_in_penultimate_position and first_type.word_after in liste_fictive + ["L", "D"]:
                return voie
        return None
