from injector import inject
from typing import List
from tqdm import tqdm

from voie_classes.decoupage_voie import DecoupageVoie
from finders.find_complement.complement_finder import ComplementFinder


class ApplyComplementFinderOnList:
    @inject
    def __init__(self, complement_finder: ComplementFinder):
        self.complement_finder: ComplementFinder = complement_finder

    def execute(
            self,
            voies_obj: List[DecoupageVoie],
            types_to_detect: List[str],
            ) -> (List[DecoupageVoie], List[DecoupageVoie]):

        voies_obj_compl = []
        new_voies_obj = voies_obj[:]
        for voie in tqdm(voies_obj):
            new_voie = self.complement_finder.execute(voie, types_to_detect)
            if new_voie:
                voies_obj_compl.append(new_voie)
                new_voies_obj.remove(voie)

        return (voies_obj_compl, new_voies_obj)
