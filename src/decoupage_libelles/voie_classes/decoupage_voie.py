from voie_classes.analysers.analyse_voie import AnalyseVoie


class DecoupageVoie(AnalyseVoie):
    """ """

    def assign_lib(self):
        self.type_assigned = ' '
        self.label_assigned = (' ').join(self.infolib.label_preproc)
        self.compl_assigned = ' '

    def assign_lib_compl(self):
        __, position_first_type_in_lib_start, __ = self.infolib.order_type_in_lib(1)
        label_assigned = (' ').join(self.infolib.get_words_between(
                                        0, position_first_type_in_lib_start))
        compl_assigned = (' ').join(self.infolib.get_words_between(
                                        position_first_type_in_lib_start))
        self.type_assigned = ' '
        self.label_assigned = label_assigned
        self.compl_assigned = compl_assigned

    def assign_compl_type_lib(self, type_order):
        type_assigned, position_type_in_lib_start, position_type_in_lib_end = self.infolib.order_type_in_lib(type_order)
        label_assigned = (' ').join(self.infolib.get_words_between(position_type_in_lib_end+1))
        compl_assigned = (' ').join(self.infolib.get_words_between(0, position_type_in_lib_start))
        self.type_assigned = type_assigned
        self.label_assigned = label_assigned
        self.compl_assigned = compl_assigned

    def assign_type_lib(self, type_order):
        type_assigned, position_type_in_lib_start, __ = self.infolib.order_type_in_lib(type_order)
        label_assigned = (' ').join(self.infolib.get_words_between(position_type_in_lib_start+1))
        self.type_assigned = type_assigned
        self.label_assigned = label_assigned
        self.compl_assigned = ' '

    def assign_type_lib_compl(
            self,
            type_order=1,
            type_order_compl=2
            ):
        type_assigned, position_type_in_lib_start, position_type_in_lib_end = self.infolib.order_type_in_lib(type_order)
        __, position_type_compl_in_lib_start,  position_type_compl_in_lib_end = self.infolib.order_type_in_lib(type_order_compl)
        label_assigned = (' ').join(
            self.infolib.get_words_between(
                position_type_in_lib_end+1,
                position_type_compl_in_lib_start)
                )
        compl_assigned = (' ').join(
            self.infolib.get_words_between(position_type_compl_in_lib_start)
            )
        self.type_assigned = type_assigned
        self.label_assigned = label_assigned
        self.compl_assigned = compl_assigned

    def assign_lib_type(self):
        type_assigned, position_type_in_lib_start, __ = self.infolib.order_type_in_lib(1)
        label_assigned = (' ').join(self.infolib.get_words_between(
            0, position_type_in_lib_start))
        self.type_assigned = type_assigned
        self.label_assigned = label_assigned
        self.compl_assigned = ' '

    def assign_compl_type_lib_compl(
            self,
            type_order,
            type_order_compl
            ):
        type_assigned, position_type_in_lib_start,  position_type_in_lib_end = self.infolib.order_type_in_lib(type_order)
        __, position_type_compl_in_lib_start, __ = self.infolib.order_type_in_lib(type_order_compl)
        compl_before = (' ').join(self.infolib.get_words_between(0, position_type_in_lib_start))
        label_assigned = (' ').join(
            self.infolib.get_words_between(
                position_type_in_lib_end+1, position_type_compl_in_lib_start)
            )
        compl_after = (' ').join(self.infolib.get_words_between(position_type_compl_in_lib_start))
        compl_assigned = compl_before + ' ' + compl_after
        self.type_assigned = type_assigned
        self.label_assigned = label_assigned
        self.compl_assigned = compl_assigned

    def not_assigned(self):
        return not self.type_assigned and not self.label_assigned and not self.compl_assigned
