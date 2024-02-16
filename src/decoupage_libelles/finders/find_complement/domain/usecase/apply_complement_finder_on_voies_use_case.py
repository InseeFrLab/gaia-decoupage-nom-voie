from injector import inject
from typing import List, Union
from tqdm import tqdm

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase


class ApplyComplementFinderOnVoiesUseCase:
    @inject
    def __init__(self, complement_finder_use_case: ComplementFinderUseCase):
        self.complement_finder_use_case: ComplementFinderUseCase = complement_finder_use_case

    def execute(
            self,
            voies_obj: List[InfoVoie],
            types_to_detect: List[str],
            ) -> Union[List[InfoVoie], List[InfoVoie]]:

        voies_obj_compl = []
        new_voies_obj = voies_obj[:]
        for voie in tqdm(voies_obj):
            new_voie = self.complement_finder_use_case.execute(voie, types_to_detect)
            if new_voie:
                voies_obj_compl.append(new_voie)
                new_voies_obj.remove(voie)

        return (voies_obj_compl, new_voies_obj)
