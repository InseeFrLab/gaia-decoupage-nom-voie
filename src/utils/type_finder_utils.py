import pandas as pd

from voie_classes.voie import Voie
from preprocessors.ponctuation_preprocessor import PonctuationPreprocessor
from constants.constant_lists import ponctuations


class TypeFinderUtils():
    def __init__(self,
                 type_voie_df: pd.DataFrame,
                 code2lib: dict,):

        self.type_voie_df = type_voie_df
        self.code2lib = code2lib
        self.codes = list(set(self.type_voie_df['CODE'].tolist()))
        self.lib2code = self.type_voie_df.set_index('LIBELLE')['CODE'].to_dict()
        self.types_lib_preproc = None
        self.types_lib_preproc2types_lib_raw = None

    def generate_type_detector_utils(self):

        types_lib = self.type_voie_df['LIBELLE'].tolist()
        types_lib = [Voie(lib_raw) for lib_raw in types_lib]
        for i, lib in enumerate(types_lib):
            lib = PonctuationPreprocessor(lib, ponctuations).run()
            types_lib[i] = lib

        types_lib_preproc_raw = [[(' ').join(elt.infolib.label_preproc),
                                  elt.label_raw] for elt in types_lib]
        types_lib_preproc2types_lib_raw = dict(types_lib_preproc_raw)

        types_lib_preproc = [(' ').join(elt.infolib.label_preproc) for elt in types_lib]
        types_lib_preproc = [elt for elt in types_lib_preproc if elt not in self.codes]

        self.types_lib_preproc2types_lib_raw = types_lib_preproc2types_lib_raw
        self.types_lib_preproc = types_lib_preproc

# Functions


def find_pos_str(
        sentence_str: str,
        str_to_find: str
        ):
    positions = []
    index = sentence_str.find(str_to_find)

    while index != -1:
        positions.append(index)
        index = sentence_str.find(str_to_find, index + 1)

    return positions


def find_pos_words(
        sentence_words: list,
        positions_letter: int
        ):
    start = 0
    for i, word in enumerate(sentence_words):
        if start == positions_letter:
            position_word = i
            break
        else:
            start += len(word) + 1
    return position_word


def min_and_max_count_espaces_in_strs(str1, str2):
    espaces_str1 = str1.count(' ')
    espaces_str2 = str2.count(' ')

    dict_two_strs = {str1: espaces_str1, str2: espaces_str2}

    str_min = min(dict_two_strs, key=dict_two_strs.get)
    str_max = max(dict_two_strs, key=dict_two_strs.get)

    return str_min, str_max


def search_pos_multi_words_type(voie, voie_sep, type_lib, type_detect, infolib):
    nb_words_in_type = len(type_lib.split(' '))
    # Dans le string du libellé de voie, on cherche le type de voie.
    # S'il n'apparaît qu'une fois, on aura la position de sa première lettre dans le
    # libellé.
    # S'il apparaît plusieurs fois, il y aura alors plusieurs positions.
    pos_debut = find_pos_str(voie, type_lib)
    for pos in pos_debut:
        # Position du premier mot du type dans le libellé découpé en mots.
        pos_type = find_pos_words(voie_sep, pos)
        if type_detect not in infolib.types_detected():
            infolib.types_and_positions[(type_detect, 1)] = (pos_type,
                                                             pos_type+nb_words_in_type-1)
        else:
            infolib.types_and_positions[(type_detect, 2)] = (pos_type,
                                                             pos_type+nb_words_in_type-1)


def remove_type_from_lib_and_types(infolib, position_start_min, position_end_min):
    # Supprimer de la liste preproc le type codifié
    before_type_min = infolib.label_preproc[:position_start_min]
    after_type_min = infolib.label_preproc[position_end_min+1:]

    infolib.label_preproc = before_type_min + after_type_min

    # Supprimer du dictionnaire le type codifié et décaler les positions
    nb_words_in_type_min = position_end_min - position_start_min + 1

    for type_lib, positions in list(infolib.types_and_positions.items()):
        position_start, position_end = positions
        if position_start > position_end_min:
            position_start -= nb_words_in_type_min
            position_end -= nb_words_in_type_min
            infolib.types_and_positions[type_lib] = (position_start,
                                                     position_end)
