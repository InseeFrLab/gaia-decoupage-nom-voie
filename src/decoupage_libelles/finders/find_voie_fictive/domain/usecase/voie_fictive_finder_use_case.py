from tqdm import tqdm
from typing import List
from injector import inject

from constants.constant_lists import list_fictive
from voie_classes.decoupage_voie import DecoupageVoie
from finders.find_voie_fictive.domain.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase
from finders.find_voie_fictive.domain.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypes


class VoieFictiveFinderUseCase:
    LISTE_FICTIVE = ['B', 'C', 'E', 'F', 'G', 'H', 'I', 'J',
                     'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                     'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', 
                     '2', '3', '4', '5', '6', '7', '8', '9']
    
    VOIES_FICTIVES_1 = ['BOULEVARD',
                        'ALLEE',
                        'RUE',
                        'AVENUE',
                        'IMPASSE',
                        'CHEMIN',
                        'VOIE',
                        'PLACE',
                        'CHEMINEMENT',
                        'VOIE COMMUNALE']

    VOIES_FICTIVES_2 = ['ROUTE',
                        'BOULEVARD',
                        'ALLEE',
                        'RUE',
                        'AVENUE',
                        'IMPASSE',
                        'CHEMIN',
                        'VOIE',
                        'PLACE',
                        'CHEMINEMENT',
                        'VOIE COMMUNALE']

    @inject
    def __init__(self,
                 detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase,
                 detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypes):
        self.detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = detect_type_fictif_for_one_type_use_case
        self.detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypes = detect_type_fictif_for_multi_types_use_case

    def execute(self,
                voie: DecoupageVoie,
                liste_voie_commun: List[str]) -> DecoupageVoie:
        nb_type = voie.infolib.nb_types_detected()
        if nb_type == 1:
            return self.detect_type_fictif_for_one_type_use_case.execute(voie, liste_voie_commun, VoieFictiveFinderUseCase.LISTE_FICTIVE)
        elif nb_type > 1:
            return self.detect_type_fictif_for_multi_types_use_case.execute(voie, liste_voie_commun, VoieFictiveFinderUseCase.LISTE_FICTIVE)
