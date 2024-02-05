from voie_classes.voie import Voie
from constants.constant_lists import liste_type_longitudinal, liste_type_longitudinal2, liste_type_agglo, liste_types_complement_0, liste_types_complement_1


class AnalyseType(Voie):

    def type_is_long(self, type_order):
        if self.infolib.nb_types_detected() == 1:
            liste_type_long = liste_type_longitudinal
        else:
            liste_type_long = liste_type_longitudinal2

        type_searched, __, __ = self.infolib.order_type_in_lib(type_order)
        return type_searched in liste_type_long

    def type_is_agglo(self, type_order):
        type_searched, __, __ = self.infolib.order_type_in_lib(type_order)
        return type_searched in liste_type_agglo

    def type_is_long_or_agglo(self, type_order):
        return self.type_is_long(type_order) or self.type_is_agglo(type_order)

    def type_is_compl(self, type_order):
        if self.infolib.nb_types_detected() == 0:
            liste_type_compl = liste_types_complement_0
        else:
            liste_type_compl = liste_types_complement_1

        type_searched, __, __ = self.infolib.order_type_in_lib(type_order)
        return type_searched in liste_type_compl
