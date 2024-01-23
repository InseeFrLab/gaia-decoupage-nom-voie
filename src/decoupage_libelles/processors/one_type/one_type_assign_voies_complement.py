from constants.constant_lists import (liste_types_compl_immeuble,
                                      liste_orthographes_immeuble
                                      )
from voie_classes.decoupage_voie import DecoupageVoie


class OneTypeAssignCompl():
    def __init__(self, voie_compl: DecoupageVoie):
        self.voie_compl = voie_compl

    def assign_if_compl_in_first_pos_and_type_in_second_pos(self):
        first_type, __, __ = self.voie_compl.infolib.order_type_in_lib(1)
        second_type, __, __ = self.voie_compl.infolib.order_type_in_lib(2)

        if self.voie_compl.type_is_compl(1):
            if first_type in liste_orthographes_immeuble:
                if second_type in liste_types_compl_immeuble:
                    # 'IMM RESIDENCE BERYL'
                    # 2eme type + lib
                    self.voie_compl.assign_type_lib(2)
                else:
                    # "IMMEUBLE VAL D'ILLAZ"
                    # lib
                    self.voie_compl.assign_lib()
            else:
                # 'LDT VAL DES PINS'
                # lib
                self.voie_compl.assign_lib()

    def assign_if_compl_in_second_pos_and_type_in_first_pos(self):
        if self.voie_compl.type_is_compl(2):
            # 'VC  LDT LA PALUN CTE CENTRALE'
            # 1er type lib
            self.voie_compl.assign_type_lib(1)

    def assign_if_compl_in_first_pos_and_type_in_last_pos(self):
        if self.voie_compl.type_is_compl(1):
            # 'IMM LE PARC'
            # lib
            self.voie_compl.assign_lib()

    def assign_if_compl_in_last_pos_and_type_in_first_pos(self):
        if self.voie_compl.type_is_compl(2):
            # 'IMP DU PAVILLON'
            # 1er type + lib
            self.voie_compl.assign_type_lib(1)

    def assign_if_compl_in_first_pos_and_type_in_middle_pos(self):
        if self.voie_compl.type_is_compl(1):
            if not self.voie_compl.has_adj_det_before_type(2):
                # 'BAT L ANJOU AVE DE VLAMINC'
                # compl + 2e type + lib
                self.voie_compl.assign_compl_type_lib(2)
            else:
                # 'IMM LE LAC DU LOU'
                # lib
                self.voie_compl.assign_lib()

    def assign_if_compl_in_middle_pos_and_type_in_first_pos(self):
        if self.voie_compl.type_is_compl(2):
            if not self.voie_compl.has_adj_det_before_type(2):
                # 'HLM LES CHARTREUX BAT B2'
                # 1er type + lib + compl
                self.voie_compl.assign_type_lib_compl()
            else:
                # 'RUE DU PAVILLON DE LA MARINE'
                # 1er type + lib
                self.voie_compl.assign_type_lib(1)

    def assign_if_compl_nor_type_not_in_first_pos(self):
        # 'LE PAVILLON DE LA FORET'
        # lib
        self.voie_compl.assign_lib()

    def run(self):
        if self.voie_compl.has_type_in_first_pos():

            if self.voie_compl.has_type_in_second_pos():
                self.assign_if_compl_in_first_pos_and_type_in_second_pos()
                self.assign_if_compl_in_second_pos_and_type_in_first_pos()

            elif self.voie_compl.has_type_in_last_pos():
                self.assign_if_compl_in_first_pos_and_type_in_last_pos()
                self.assign_if_compl_in_last_pos_and_type_in_first_pos()

            elif self.voie_compl.has_type_in_middle_pos(2):
                self.assign_if_compl_in_first_pos_and_type_in_middle_pos()
                self.assign_if_compl_in_middle_pos_and_type_in_first_pos()

        else:
            self.assign_if_compl_nor_type_not_in_first_pos()
