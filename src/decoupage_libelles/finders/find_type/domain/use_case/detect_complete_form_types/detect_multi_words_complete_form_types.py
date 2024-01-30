from utils.type_finder_utils import (find_pos_str,
                                     find_pos_words)
from finders.find_type.domain.model.type_finder_object import TypeFinderObject


class DetectMultiWordsCompleteFormTypes:

    def execute(self,
                type_detect: str,
                type_lib: str,
                type_finder_object: TypeFinderObject) -> TypeFinderObject:
            nb_words_in_type = len(type_lib.split(' '))

            pos_debut = find_pos_str(type_finder_object.voie, type_lib)
            for pos in pos_debut:
                pos_type = find_pos_words(type_finder_object.voie_sep, pos)
                if type_detect not in type_finder_object.infolib.types_detected():
                    type_finder_object.infolib.types_and_positions[(type_detect, 1)] = (pos_type,
                                                                    pos_type+nb_words_in_type-1)
                else:
                    type_finder_object.infolib.types_and_positions[(type_detect, 2)] = (pos_type,
                                                                    pos_type+nb_words_in_type-1)
            return type_finder_object
