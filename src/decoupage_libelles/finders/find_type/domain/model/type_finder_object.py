from dataclasses import dataclass
from typing import List

from voie_classes.voie import Voie
from finders.find_type.domain.usecase.generate_type_finder_utils_use_case import TypeFinderUtils
from voie_classes.informations_on_libelle import InfoLib


@dataclass
class TypeFinderObject:
    voie_big: Voie
    type_data: TypeFinderUtils
    voie_sep: List[str] = voie_big.infolib.label_preproc[:]
    voie: str = (' ').join(voie_big.infolib.label_preproc[:])
    infolib: InfoLib = InfoLib(voie_sep)
