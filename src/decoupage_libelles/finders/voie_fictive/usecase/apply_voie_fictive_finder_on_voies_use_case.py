from typing import List, Union

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.finders.voie_fictive.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase


class ApplyVoieFictiveFinderOnVoiesUseCase:
    def __init__(
        self,
        voie_fictive_finder_use_case: VoieFictiveFinderUseCase = VoieFictiveFinderUseCase(),
        generate_information_on_lib_use_case : GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase()
    ):
        self.voie_fictive_finder_use_case: VoieFictiveFinderUseCase = voie_fictive_finder_use_case
        self.generate_information_on_lib_use_case : GenerateInformationOnLibUseCase = generate_information_on_lib_use_case

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
                self.generate_information_on_lib_use_case.execute(new_voie, apply_nlp_model=False)
                list_object_voies_fictives.append(new_voie)
                new_list_object_voies.remove(voie)

        return (list_object_voies_fictives, new_list_object_voies)
