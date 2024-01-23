from voie_classes.decoupage_voie import DecoupageVoie


class NoTypeAssignCompl():
    def __init__(self, voie_compl: DecoupageVoie):
        self.voie_compl = voie_compl

    def assign_if_not_adj_before_type_compl(self):
        if (self.voie_compl.has_type_in_middle_pos(1) and
                not self.voie_compl.has_adj_det_before_type(1)):
            print('couc')
            # 'LE TILLET BAT A'
            # lib + compl
            self.voie_compl.assign_lib_compl()

    def assign_if_type_first_pos_or_adj_before_type_compl(self):
        if (not self.voie_compl.has_type_in_middle_pos(1) or
                self.voie_compl.has_type_in_middle_pos(1) and
                self.voie_compl.has_adj_det_before_type(1)):
            # 'BAT JEAN LAMOUR'
            # lib
            self.voie_compl.assign_lib()

    def run(self):
        self.assign_if_not_adj_before_type_compl()
        self.assign_if_type_first_pos_or_adj_before_type_compl()
