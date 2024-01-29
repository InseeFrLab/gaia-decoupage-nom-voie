from voie_classes.voie import Voie
from utils.type_finder_utils import TypeFinderUtils
from voie_classes.informations_on_libelle import InfoLib

class DetectCodifiedTypes():
    def execute(self,
                 voie_big: Voie,
                 type_data: TypeFinderUtils) -> InfoLib:
        voie_sep = voie_big.infolib.label_preproc[:]
        infolib = InfoLib(voie_sep)

        for code_type in type_data.codes:
            lib_type = type_data.code2lib[code_type]
            if code_type in voie_sep:
                pos_type = [i for i, mot in enumerate(voie_sep) if mot == code_type]
                for position in pos_type:
                    positions = (position,
                                 position)
                    if lib_type not in infolib.types_detected():
                        infolib.types_and_positions[(lib_type, 1)] = positions
                    else:
                        infolib.types_and_positions[(lib_type, 2)] = positions
        return infolib