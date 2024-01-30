from tqdm import tqdm
from typing import List
from injector import inject

from constants.constant_lists import list_fictive
from voie_classes.decoupage_voie import DecoupageVoie
from finders.find_voie_fictive.domain.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase
from finders.find_voie_fictive.domain.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypes


class VoieFictiveFinderUseCase:
    @inject
    def __init__(self,
                 detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase,
                 detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypes):
        self.detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = detect_type_fictif_for_one_type_use_case
        self.detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypes = detect_type_fictif_for_multi_types_use_case

    def execute(self,
                voie: DecoupageVoie,
                liste_voie_commun: List[str]):
        nb_type = voie.infolib.nb_types_detected()
        if nb_type == 1:
            return self.detect_type_fictif_for_one_type_use_case.execute(voie, liste_voie_commun)
        elif nb_type > 1:
            return self.detect_type_fictif_for_multi_types_use_case.execute(voie, liste_voie_commun)
