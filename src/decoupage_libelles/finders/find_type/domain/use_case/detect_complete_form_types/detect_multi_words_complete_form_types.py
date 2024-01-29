from voie_classes.voie import Voie
from utils.type_finder_utils import (TypeFinderUtils,
                                     find_pos_str,
                                     find_pos_words)
from voie_classes.informations_on_libelle import InfoLib


class detect_multi_words_complete_form_types:

    def execute(self,
                type_detect: str,
                type_lib: str,
                voie_big: Voie,
                type_data: TypeFinderUtils, 
                infolib: InfoLib):
            voie_sep = voie_big.infolib.label_preproc[:]
            voie = (' ').join(voie_sep)
            nb_words_in_type = len(type_lib.split(' '))

            pos_debut = find_pos_str(voie, type_lib)
            for pos in pos_debut:
                pos_type = find_pos_words(voie_sep, pos)
                if type_detect not in infolib.types_detected():
                    infolib.types_and_positions[(type_detect, 1)] = (pos_type,
                                                                    pos_type+nb_words_in_type-1)
                else:
                    infolib.types_and_positions[(type_detect, 2)] = (pos_type,
                                                                    pos_type+nb_words_in_type-1)
