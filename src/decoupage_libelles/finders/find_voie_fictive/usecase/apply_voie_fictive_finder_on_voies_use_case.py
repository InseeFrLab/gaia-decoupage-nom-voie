from typing import List, Union

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_voie_fictive.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase


class ApplyVoieFictiveFinderOnVoiesUseCase:
    def __init__(self, voie_fictive_finder_use_case: VoieFictiveFinderUseCase = VoieFictiveFinderUseCase()):
        self.voie_fictive_finder_use_case: VoieFictiveFinderUseCase = voie_fictive_finder_use_case

    def execute(
        self,
        list_object_voies: List[InfoVoie],
        list_type_to_detect: List[str],
    ) -> Union[List[InfoVoie], List[InfoVoie]]:
        list_object_voies_fictives = []
        new_list_object_voies = list_object_voies[:]
        for voie in list_object_voies:
            new_voie = self.voie_fictive_finder_use_case.execute(voie, list_type_to_detect)
            if new_voie:
                list_object_voies_fictives.append(new_voie)
                new_list_object_voies.remove(voie)

        return (list_object_voies_fictives, new_list_object_voies)
