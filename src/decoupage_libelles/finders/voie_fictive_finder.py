from tqdm import tqdm
from typing import List

from constants.constant_lists import list_fictive
from voie_classes.decoupage_voie import DecoupageVoie


class VoieFictiveFinder():
    def __init__(self,
                 voie: DecoupageVoie,
                 liste_voie_commun: list):
        self.voie = voie
        self.infolib = self.voie.infolib
        self.liste_voie_commun = liste_voie_commun
        self.nb_type = voie.infolib.nb_types_detected()
        self.has_type_fictif = False

    def detect_only_type_fictif(self):
        # si RUE A on garde type 'RUE' et libellé 'A'. Si il y a qlq chose avant 'RUE',
        # alors ca passe en voie fictive
        if self.nb_type == 1:
            for type_voie in self.liste_voie_commun:
                first_type, __, __ = self.infolib.order_type_in_lib(1)
                if (first_type == type_voie and
                        self.voie.has_type_in_penultimate_pos(1) and
                        self.voie.word_before_type(1) and
                        self.voie.word_after_type(1) in list_fictive+['L', 'D', 'A']):
                    self.has_type_fictif = True

    def detect_multi_types_fictif(self):
        if self.nb_type > 1:
            for type_voie in self.liste_voie_commun:
                if type_voie in self.infolib.types_detected():
                    for occurence in range(1, 3):
                        if (type_voie, occurence) in self.infolib.types_and_positions:
                            type_fictif = (type_voie, occurence)
                            position_start, __ = self.infolib.types_and_positions[type_fictif]

                            type_after = self.infolib.type_after_type(type_voie, 1)
                            if type_after:
                                position_end = self.infolib.types_and_positions[type_after][0]-1
                            else:
                                position_end = len(self.infolib.label_preproc)+1

                            elt_fictif = self.infolib.get_words_between(
                                            position_start+1,
                                            position_end)

                            one_word_label_fictif = True if len(elt_fictif) == 1 else False
                            has_type_fictif_in_last_pos = (True
                                                           if not type_after
                                                           else False)

                            if one_word_label_fictif:
                                if (elt_fictif[0] in list_fictive or
                                        elt_fictif[0] in ['L', 'D', 'A'] and
                                        has_type_fictif_in_last_pos):
                                    self.has_type_fictif = True

    def run(self):
        self.detect_only_type_fictif()
        self.detect_multi_types_fictif()
        if self.has_type_fictif:
            return self.voie

    @staticmethod
    def apply_find_voies_fictives_on_list(
            list_object_voies: List[DecoupageVoie],
            list_type_to_detect: list,
            ):

        list_object_voies_fictives = []
        new_list_object_voies = list_object_voies[:]
        for voie in tqdm(list_object_voies):
            new_voie = VoieFictiveFinder(voie, list_type_to_detect).run()
            if new_voie:
                list_object_voies_fictives.append(new_voie)
                new_list_object_voies.remove(voie)

        return (list_object_voies_fictives, new_list_object_voies)
