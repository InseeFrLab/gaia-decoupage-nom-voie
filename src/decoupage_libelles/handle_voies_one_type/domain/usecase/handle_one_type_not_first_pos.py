class HandleOneTypeNotFirstPos():


    def assign_if_type_is_route(self):
        first_type, __, __ = self.voie.infolib.order_type_in_lib(1)

        if (first_type == 'ROUTE' and
                self.voie.word_before_type(1) in ['C', 'N', 'D'] or
                first_type == 'ROUTE' and
                self.voie.word_after_type(1) in ['C', 'N', 'D']):
            # 1 er type + lib
            # test = VoieType('N RTE NATIONALE 9', ['N', 'RTE', 'NATIONALE', '9'], ['ROUTE'], [1], ['PRON', 'PRON', 'ADJ', 'NUM'])
            self.voie.assign_type_lib(1)

    def assign_if_type_is_agglo(self):
        if (self.voie.type_is_agglo(1) and
                not self.voie.has_adj_det_before_type(1) and
                self.voie.has_type_in_last_pos()):
            # lib + 1er type
            # test = VoieType('AVILLON HAM', ['AVILLON', 'HAM'], ['HAMEAU'], [1], ['PROPN', 'PROPN'])
            self.voie.assign_lib_type()

    def assign_rest(self):
        if self.voie.not_assigned():
            # lib
            # test = VoieType('LE CHEMIN DE L ETOILE', ['LE', 'CHEMIN', 'DE', 'L', 'ETOILE'], ['CHEMIN'], [1]], ['DET', 'NOUN', 'ADP', 'DET', 'NOUN'])
            self.voie.assign_lib()

    def run(self):
        self.assign_if_type_is_long()
        self.assign_if_type_is_route()
        self.assign_if_type_is_agglo()
        self.assign_rest()
