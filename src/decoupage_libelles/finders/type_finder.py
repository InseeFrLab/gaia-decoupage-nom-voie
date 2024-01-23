from voie_classes.voie import Voie
from utils.utils_for_lists import list_incluse
from utils.type_finder_utils import (TypeFinderUtils,
                                     search_pos_multi_words_type,
                                     remove_type_from_lib_and_types,
                                     min_and_max_count_espaces_in_strs)
from voie_classes.informations_on_libelle import InfoLib


class TypeFinder():
    def __init__(self,
                 voie_big: Voie,
                 type_data: TypeFinderUtils):

        self.voie_big = voie_big
        self.type_data = type_data

        self.original_voie_sep = voie_big.infolib.label_preproc
        self.voie_sep = voie_big.infolib.label_preproc[:]
        self.voie = (' ').join(voie_big.infolib.label_preproc[:])
        self.infolib = InfoLib(self.original_voie_sep)

    def detect_codified_types(self):
        for code_type in self.type_data.codes:
            lib_type = self.type_data.code2lib[code_type]
            if code_type in self.original_voie_sep:
                pos_type = [i for i, mot in enumerate(self.original_voie_sep) if mot == code_type]
                for position in pos_type:
                    positions = (position,
                                 position)
                    if lib_type not in self.infolib.types_detected():
                        self.infolib.types_and_positions[(lib_type, 1)] = positions
                    else:
                        self.infolib.types_and_positions[(lib_type, 2)] = positions

    def detect_complete_form_types(self):
        for type_lib in self.type_data.types_lib_preproc:
            type_detect = self.type_data.types_lib_preproc2types_lib_raw[type_lib]
            type_detect = self.type_data.lib2code[type_detect]
            type_detect = self.type_data.code2lib[type_detect]
            nb_words_in_type = len(type_lib.split(' '))
            # Si le type ne s'écrit qu'en 1 mot
            if type_lib in self.voie_sep and nb_words_in_type == 1:
                pos_type = [i for i, mot in enumerate(self.voie_sep) if mot == type_lib]
                for pos in pos_type:
                    positions = (pos, pos)
                    if type_detect not in self.infolib.types_detected():
                        self.infolib.types_and_positions[(type_detect, 1)] = positions
                    else:
                        self.infolib.types_and_positions[(type_detect, 2)] = positions

            # Si le type s'écrit en plusieurs mots
            elif (type_lib in self.voie and
                  nb_words_in_type > 1 and
                  list_incluse(type_lib.split(' '), self.voie_sep)):
                search_pos_multi_words_type(self.voie,
                                            self.original_voie_sep,
                                            type_lib,
                                            type_detect,
                                            self.infolib)

    def update_occurences_by_order_of_apparition(self):
        self.infolib.sort_types_by_position()
        sorted_keys = self.infolib.types_and_positions.keys()

        new_types_and_positions = {}
        occurrences = {}

        for key in sorted_keys:
            type_voie = key[0]
            if type_voie in occurrences:
                occurrences[type_voie] += 1
            else:
                occurrences[type_voie] = 1

            new_key = (type_voie, occurrences[type_voie])
            new_types_and_positions[new_key] = self.infolib.types_and_positions[key]

        self.infolib.types_and_positions = new_types_and_positions

    def remove_duplicates(self):
        # Supprime les doublons de type détectés causés par l'algorithme ou par une erreur de
        # saisie de libellé Majic (ex : CR CHEMIN RURAL NO 15)
        if self.infolib.has_duplicates():
            types_duplicates = [type_lib for type_lib, occurence in self.infolib.types_and_positions if occurence > 1]

            for type_duplicate in types_duplicates:
                dict_two_positions = {'first': self.infolib.types_and_positions[(type_duplicate, 1)],
                                      'second': self.infolib.types_and_positions[(type_duplicate, 2)]}
                dist_positions = dict_two_positions['second'][0] - dict_two_positions['first'][1]

                if dist_positions == 1:
                    type_min_distance = min(dict_two_positions, key=lambda k: dict_two_positions[k][1] - dict_two_positions[k][0])

                    position_start_min, position_end_min = dict_two_positions[type_min_distance]

                    # Supprimer de la liste preproc le type codifié
                    # Supprimer du dictionnaire le type codifié et décaler les positions
                    remove_type_from_lib_and_types(self.infolib,
                                                   position_start_min,
                                                   position_end_min)

                    if type_min_distance == "first":
                        del self.infolib.types_and_positions[(type_duplicate, 1)]
                        self.infolib.types_and_positions[(type_duplicate, 1)] = self.infolib.types_and_positions[(type_duplicate, 2)]
                        del self.infolib.types_and_positions[(type_duplicate, 2)]
                    else:
                        del self.infolib.types_and_positions[(type_duplicate, 2)]

    def remove_wrong_detected_codes(self):
        # Supprime les types codifiés détectés à tord
        # (ex : ANC CHEM --> ANCIEN CHEMIN et CHEMINEMENT)
        for i in range(1, len(self.infolib.types_and_positions)):
            dict_two_types = {}

            type_i, position_start_i, position_end_i = self.infolib.order_type_in_lib(i)
            type_i1, position_start_i1, position_end_i1 = self.infolib.order_type_in_lib(i+1)

            dict_two_types[type_i] = (position_start_i, position_end_i)
            dict_two_types[type_i1] = (position_start_i1, position_end_i1)

            type_min, type_max = min_and_max_count_espaces_in_strs(type_i, type_i1)

            position_start_min, __ = dict_two_types[type_min]
            position_start_max, position_end_max = dict_two_types[type_max]

            if position_start_min in list(range(position_start_max, position_end_max + 1)):
                del self.infolib.types_and_positions[(type_min, 1)]

    def run(self):
        self.detect_codified_types()
        self.detect_complete_form_types()
        if self.infolib.nb_types_detected() > 1:
            self.sort_by_position()
            self.update_occurences_by_order_of_apparition()
            self.remove_duplicates()
            self.remove_wrong_detected_codes()
        self.voie_big.infolib = self.infolib
        return self.voie_big


# Utilisation
# type_finder = TypeFinder(voie_big, type_voie_df, code2lib)
# type_finder.run()
# voie_big = type_finder.voie_big
