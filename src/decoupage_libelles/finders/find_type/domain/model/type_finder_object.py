from dataclasses import dataclass

from voie_classes.voie import Voie
from utils.type_finder_utils import TypeFinderUtils
from voie_classes.informations_on_libelle import InfoLib


@dataclass
class TypeFinderObject:
    voie_big: Voie
    type_data: TypeFinderUtils
    voie_sep = voie_big.infolib.label_preproc[:]
    voie = (' ').join(voie_big.infolib.label_preproc[:])
    infolib = InfoLib(voie_sep)
