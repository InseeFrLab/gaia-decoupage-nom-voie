from voie_classes.voie import Voie
from utils.type_finder_utils import TypeFinderUtils
from voie_classes.informations_on_libelle import InfoLib


class DetectOneWordCompleteFormTypes:
    def execute(self,
                type_detect: str,
                type_lib: str,
                voie_big: Voie,
                type_data: TypeFinderUtils, 
                infolib: InfoLib):
            voie_sep = voie_big.infolib.label_preproc[:]
            pos_type = [i for i, mot in enumerate(voie_sep) if mot == type_lib]
            for pos in pos_type:
                positions = (pos, pos)
                if type_detect not in infolib.types_detected():
                    infolib.types_and_positions[(type_detect, 1)] = positions
                else:
                    infolib.types_and_positions[(type_detect, 2)] = positions