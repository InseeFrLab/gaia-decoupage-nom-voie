from typing import List
from tqdm import tqdm

from voie_classes.decoupage_voie import DecoupageVoie
from finders.find_complement.complement_finder import ComplementFinder
from finders.voie_fictive_finder import VoieFictiveFinder

from constants.constant_lists import (liste_types_complement_1,
                                      liste_voie_fictive_2,
                                      first_type_agglo,
                                      liste_types_compl_immeuble
                                      )
from constants.constant_dicts import combinaisons_long


class TwoTypesVoiesHandler():
    def __init__(self,
                 voies: List[DecoupageVoie]):
        self.voies = [voie for voie in voies if (voie.infolib.nb_types_detected() == 2 and
                                                 voie.not_assigned())]
        self.voies_complement = None
        self.voies_fictives = None

    def handle_voies_complementaires(self):
        self.voies_complement, self.voies = ComplementFinder.apply_find_type_complement_on_list(
                                            self.voies,
                                            liste_types_complement_1
                                            )
        for voie in self.voies_complement:
            if (voie.types_detected[0] in liste_types_complement_1 and
                    voie.has_type_in_first_pos() and
                    voie.has_type_in_second_pos() and
                    voie.types_detected[1] in liste_types_compl_immeuble):
                # 'IMM RES DU CENTRE RUE DE BRAS'
                # supprimer le type complement devant et repasser à deux types
                voie.label_preproc = voie.label_preproc[1:]
                voie.types_detected = voie.types_detected[1:]
                voie.position_types = voie.position_types[1:]
                voie.position_types = [position-1 for position in voie.position_types]
                self.voies.append(voie)
                self.voies_complement.remove(voie)

            elif (voie.type_is_long_or_agglo(0) and voie.type_is_long_or_agglo(1) or
                    voie.type_is_long_or_agglo(0) and voie.type_is_long_or_agglo(2) or
                    voie.type_is_long_or_agglo(1) and voie.type_is_long_or_agglo(2)):
                if (voie.type_is_agglo(0) and
                        voie.type_is_long(1)):
                    # 'HLM AVE KLEBER BAT DESCARTES'
                    # compl + 2e type + lib + 3e type compl
                    voie.assign_compl_type_lib_compl(1, 2)
                elif (voie.type_is_agglo(0) and
                      voie.type_is_long(2) or
                      voie.type_is_agglo(1) and
                      voie.type_is_long(2)):
                    # compl + 3e type + lib
                    voie.assign_compl_type_lib(2)
                elif (voie.type_is_agglo(1) and
                      voie.type_is_long(0) or
                      voie.type_is_agglo(2) and
                      voie.type_is_long(0)):
                    # 1er type + lib + 2e type compl
                    voie.assign_type_lib_compl()
                else:
                    # IMM BLEU RUE DES LYS RESIDENCE ERNEST RENAN
                    # compl + 2e type + lib + 3e compl
                    voie.assign_compl_type_lib_compl(1, 2)

            elif (voie.type_is_long_or_agglo(0) or
                  voie.type_is_long_or_agglo(1) or
                  voie.type_is_long_or_agglo(2)):

                if voie.types_detected[0] in liste_types_complement_1:
                    if voie.type_is_long_or_agglo(1):
                        # compl + 2e type + lib
                        voie.assign_compl_type_lib(1)
                    elif voie.type_is_long_or_agglo(2):  # else
                        # compl + 3e type + lib
                        voie.assign_compl_type_lib(2)

                elif voie.types_detected[1] in liste_types_complement_1:
                    if voie.type_is_long_or_agglo(0):
                        # 1er type + lib + 2e type compl
                        voie.assign_type_lib_compl()
                    elif voie.type_is_long_or_agglo(2):  # else
                        # lib
                        voie.assign_lib()

                elif voie.types_detected[2] in liste_types_complement_1:
                    if voie.type_is_long_or_agglo(0):
                        # 1er type + lib + 3e type compl
                        voie.assign_type_lib_comp(0, 2)
                    if voie.type_is_long_or_agglo(1):
                        # lib
                        voie.assign_lib()

            else:
                # lib
                voie.assign_lib()

    def handle_voies_fictives(self):
        self.voies_fictives, self.voies = VoieFictiveFinder.apply_find_voies_fictives_on_list(
                                          self.voies,
                                          liste_voie_fictive_2
                                          )
        for voie in self.voies_fictives:
            if voie.position_types[1] - voie.position_types[0] > 2:
                # 1er type + lib + compl
                voie.assign_type_lib_compl()
            else:
                position_between_types = voie.position_types[1]-1
                elt_between_types = voie.label_preproc[position_between_types]
                if len(elt_between_types) == 1:
                    # compl + 2e type + lib
                    voie.assign_compl_type_lib(1)
                else:
                    # 1er type + lib + compl
                    voie.assign_type_lib_compl()

    def handle_voies_type_first_pos(self):
        voies_type_first_pos = [voie for voie in self.voies if voie.has_type_in_first_pos()]
        for voie in tqdm(voies_type_first_pos):
            if (voie.has_type_in_second_pos() or
                    voie.has_type_in_last_pos()):
                # 1er type + lib
                voie.assign_type_lib(0)

            else:

                if (not voie.type_is_long_or_agglo(0) and
                        not voie.type_is_long_or_agglo(1) or
                        voie.type_is_long_or_agglo(0) and
                        not voie.type_is_long_or_agglo(1)):
                    # 1er type + lib
                    voie.assign_type_lib(0)

                elif (not voie.type_is_long_or_agglo(0) and
                        voie.type_is_long_or_agglo(1)):
                    if voie.has_adj_det_before_type(1):
                        # 1er type + lib
                        voie.assign_type_lib(0)
                    else:
                        # compl + 2e type + lib
                        voie.assign_compl_type_lib(1)

                else:
                    if voie.has_adj_det_before_type(1):
                        # 1er type + lib
                        voie.assign_type_lib(0)

                    else:
                        if (voie.type_is_agglo(0) and
                                voie.type_is_long(1)):
                            # compl + 2e type + lib
                            voie.assign_compl_type_lib(1)

                        elif (voie.type_is_long(0) and
                              voie.type_is_long(1)):
                            two_longs = ("/").join(voie.types_detected)
                            if voie.types_detected[0] == voie.types_detected[1]:
                                # lib
                                voie.assign_lib()

                            elif (two_longs in combinaisons_long and
                                  not combinaisons_long[two_longs]):
                                # compl + 2e type + lib
                                voie.assign_compl_type_lib(1)
                            else:
                                # 1er type + lib + compl
                                voie.assign_type_lib_compl()

                        elif (voie.type_is_agglo(0) and
                              voie.type_is_agglo(1)):
                            if voie.types_detected[0] == voie.types_detected[1]:
                                # lib
                                voie.assign_lib()
                            elif voie.types_detected[1] in first_type_agglo:
                                # compl + 2e type + lib
                                voie.assign_compl_type_lib(1)
                            else:
                                # 1er type + lib + compl
                                voie.assign_type_lib_compl()

                        else:  # si le premier est long et le deuxieme agglo
                            # 1er type + lib + compl
                            voie.assign_type_lib_compl()

    def handle_voies_type_not_first_pos(self):
        voies_type_not_first_pos = [voie for voie in self.voies if voie.has_type_in_middle_pos(0)]
        for voie in tqdm(voies_type_not_first_pos):
            if voie.has_type_in_last_pos():
                if voie.has_adj_det_before_type(1):
                    # lib
                    voie.assign_lib()

                else:
                    if voie.has_type_in_penultimate_pos(0):
                        # lib
                        voie.assign_lib()
                    else:
                        # compl + 1er type + lib
                        voie.assign_compl_type_lib(0)

            else:
                if (not voie.type_is_long_or_agglo(0) and
                        not voie.type_is_long_or_agglo(1)):
                    # lib
                    voie.assign_lib()

                elif (voie.type_is_long_or_agglo(0) and
                      not voie.type_is_long_or_agglo(1)):
                    if voie.has_adj_det_before_type(0):
                        # lib
                        voie.assign_lib()
                    else:
                        # compl + 1er type + lib
                        voie.assign_compl_type_lib(0)

                elif (not voie.type_is_long_or_agglo(0) and
                      voie.type_is_long_or_agglo(1)):
                    # lib
                    voie.assign_lib()
                else:
                    if voie.has_adj_det_before_type(0):
                        # lib
                        voie.assign_lib()

                    else:
                        if voie.type_is_long(0):
                            # compl + 1er type + lib
                            voie.assign_compl_type_lib(0)
                        elif voie.type_is_agglo(0):  # équivalent à else
                            # compl + 2e type + lib
                            voie.assign_compl_type_lib(1)

    def run(self):
        print("Gestion des voies avec complément")
        self.handle_voies_complementaires()
        print("Gestion des voies fictives")
        self.handle_voies_fictives()
        print("Gestion des voies avec un type en première position")
        print("Étape longue")
        self.handle_voies_type_first_pos()
        print("Gestion des voies sans type en première position")
        self.handle_voies_type_not_first_pos()
        voies_traited = self.voies + self.voies_complement + self.voies_fictives
        return voies_traited
