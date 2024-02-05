from voie_classes.voie import Voie
from utils.utils_for_lists import is_last_position
from voie_classes.informations_on_libelle import InfoLib

class AnalysePosition:
    
    def __init__(self):
        
        
    def execute(self, infolib: InfoLib):
        
    
    def has_type_in_first_pos(self):
        __, position_first_type_in_lib_start, __ = self.infolib.order_type_in_lib(1)
        return position_first_type_in_lib_start == 0

    def has_type_in_second_pos(self, type_order=2):
        __, position_type_in_lib_start, __ = self.infolib.order_type_in_lib(type_order)
        return position_type_in_lib_start == 1

    def has_type_in_middle_pos(self, type_order):
        __, position_middle_type_in_lib_start, __ = self.infolib.order_type_in_lib(type_order)
        return (type_order-1 < position_middle_type_in_lib_start and
                not is_last_position(self.infolib.label_preproc, position_middle_type_in_lib_start))

    def has_type_in_penultimate_pos(self, type_order):
        __, __, position_penultimate_type_in_lib_end = self.infolib.order_type_in_lib(type_order)
        return position_penultimate_type_in_lib_end == len(self.infolib.label_preproc)-2

    def has_type_in_last_pos(self):
        __, __, position_last_type_in_lib_end = self.infolib.order_type_in_lib(-1)
        return is_last_position(self.infolib.label_preproc, position_last_type_in_lib_end)
