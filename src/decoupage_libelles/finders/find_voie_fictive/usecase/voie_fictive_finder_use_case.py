from typing import List

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_voie_fictive.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase
from decoupage_libelles.finders.find_voie_fictive.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypesUseCase


class VoieFictiveFinderUseCase:
    LISTE_FICTIVE = ["A", "B", "C", "E", "F", "G", "H", "I", "J", "K", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    VOIES_FICTIVES_1 = ["BOULEVARD", "ALLEE", "RUE", "AVENUE", "IMPASSE", "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE", "BATIMENT"]

    VOIES_FICTIVES_2 = ["ROUTE", "BOULEVARD", "ALLEE", "RUE", "AVENUE", "IMPASSE", "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE", "BATIMENT"]

    def __init__(
        self,
        detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = DetectTypeFictifForOneTypeUseCase(),
        detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypesUseCase = DetectTypeFictifForMultiTypesUseCase(),
    ):
        self.detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = detect_type_fictif_for_one_type_use_case
        self.detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypesUseCase = detect_type_fictif_for_multi_types_use_case

    def execute(self, voie: InfoVoie, liste_voie_commun: List[str]) -> InfoVoie:
        if len(voie.types_and_positions) == 1:
            return self.detect_type_fictif_for_one_type_use_case.execute(voie, liste_voie_commun, VoieFictiveFinderUseCase.LISTE_FICTIVE)
        elif len(voie.types_and_positions) > 1:
            return self.detect_type_fictif_for_multi_types_use_case.execute(voie, liste_voie_commun, VoieFictiveFinderUseCase.LISTE_FICTIVE)
