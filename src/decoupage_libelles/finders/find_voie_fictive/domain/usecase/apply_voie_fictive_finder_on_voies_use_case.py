from typing import List, Union
from injector import inject
from tqdm import tqdm

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from finders.find_voie_fictive.domain.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase


class ApplyVoieFictiveFinderOnVoiesUseCase:
    @inject
    def __init__(self, voie_fictive_finder_use_case: VoieFictiveFinderUseCase):
        self.voie_fictive_finder_use_case: VoieFictiveFinderUseCase = voie_fictive_finder_use_case

    def execute(self,
            list_object_voies: List[InfoVoie],
            list_type_to_detect: List[str],
            ) -> Union[List[InfoVoie], List[InfoVoie]]:

        list_object_voies_fictives = []
        new_list_object_voies = list_object_voies[:]
        for voie in tqdm(list_object_voies):
            new_voie = self.voie_fictive_finder_use_case.execute(voie, list_type_to_detect)
            if new_voie:
                list_object_voies_fictives.append(new_voie)
                new_list_object_voies.remove(voie)

        return (list_object_voies_fictives, new_list_object_voies)
