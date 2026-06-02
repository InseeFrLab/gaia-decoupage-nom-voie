from typing import List, Union, Optional

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.finders.complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase


class ApplyComplementFinderOnVoiesUseCase:
    def __init__(
        self,
        complement_finder_use_case: ComplementFinderUseCase = ComplementFinderUseCase(),
        generate_information_on_lib_use_case : GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase()
    ):
        self.complement_finder_use_case: ComplementFinderUseCase = complement_finder_use_case
        self.generate_information_on_lib_use_case : GenerateInformationOnLibUseCase = generate_information_on_lib_use_case

    def execute(
        self,
        voies_obj: List[InfoVoie],
        types_to_detect: List[str],
    ) -> Union[List[InfoVoie], List[InfoVoie]]:
        voies_obj_compl = []
        new_voies_obj = voies_obj[:]
        for voie in voies_obj:
            new_voie: Optional[InfoVoie] = self.complement_finder_use_case.execute(voie, types_to_detect)
            if new_voie:
                self.generate_information_on_lib_use_case.execute(new_voie, apply_nlp_model=False)
                voies_obj_compl.append(new_voie)
                new_voies_obj.remove(voie)

        return (voies_obj_compl, new_voies_obj)
