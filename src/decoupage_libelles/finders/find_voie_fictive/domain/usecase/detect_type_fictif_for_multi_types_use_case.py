from typing import List

from voie_classes.decoupage_voie import DecoupageVoie


class DetectTypeFictifForMultiTypes:
    def execute(self,
                voie: DecoupageVoie,
                liste_voie_commun: List[str],
                liste_fictive: List[str]) -> DecoupageVoie:
            
            for type_voie in liste_voie_commun:
                if type_voie in voie.infolib.types_detected():
                    for occurence in range(1, 3):
                        if (type_voie, occurence) in voie.infolib.types_and_positions:
                            type_fictif = (type_voie, occurence)
                            position_start, __ = voie.infolib.types_and_positions[type_fictif]

                            type_after = voie.infolib.type_after_type(type_voie, 1)

                            position_end = (voie.infolib.types_and_positions[type_after][0]-1
                                            if type_after
                                            else len(voie.infolib.label_preproc)+1)

                            elt_fictif = voie.infolib.get_words_between(
                                            position_start+1,
                                            position_end)

                            one_word_label_fictif = True if len(elt_fictif) == 1 else False
                            has_type_fictif_in_last_pos = (True
                                                        if not type_after
                                                        else False)

                            if (one_word_label_fictif and 
                                    elt_fictif[0] in liste_fictive or
                                    one_word_label_fictif and
                                    elt_fictif[0] in ['L', 'D', 'A'] and
                                    has_type_fictif_in_last_pos):
                                return voie