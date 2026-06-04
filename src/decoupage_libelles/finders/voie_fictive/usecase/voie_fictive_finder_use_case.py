from typing import List

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.finders.voie_fictive.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase
from decoupage_libelles.finders.voie_fictive.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypesUseCase
from decoupage_libelles.synonym_data.voies_fictives import LISTE_FICTIVE


class VoieFictiveFinderUseCase:
    def __init__(
        self,
        detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = DetectTypeFictifForOneTypeUseCase(),
        detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypesUseCase = DetectTypeFictifForMultiTypesUseCase(),
    ):
        self.detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = detect_type_fictif_for_one_type_use_case
        self.detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypesUseCase = detect_type_fictif_for_multi_types_use_case

    def execute(self, voie: InfoVoie, liste_voie_commun: List[str]) -> InfoVoie:
        if len(voie.types_and_positions) == 1:
            return self.detect_type_fictif_for_one_type_use_case.execute(voie, liste_voie_commun, LISTE_FICTIVE)
        elif len(voie.types_and_positions) > 1:
            return self.detect_type_fictif_for_multi_types_use_case.execute(voie, liste_voie_commun, LISTE_FICTIVE)
