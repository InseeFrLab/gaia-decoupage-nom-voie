from injector import inject

from informations_on_lib.analyse_type.analyse_position.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib


class PositionOfTypesInLibAnalyserUseCase:
    @inject
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib):
         self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infolib: InfoLib) -> InfoLib:

        type_ordered_first = self.order_type_in_lib_use_case.execute(infolib, 1)
        if type_ordered_first and type_ordered_first.position_start == 0:
            infolib.has_type_in_first_pos = True
        
        type_ordered_second = self.order_type_in_lib_use_case.execute(infolib, 2)
        if type_ordered_second and type_ordered_second.position_start == 1:
            infolib.has_type_in_second_pos = True
        
        type_ordered_last = self.order_type_in_lib_use_case.execute(infolib, -1)
        if type_ordered_last and type_ordered_last.position_end==len(infolib.label_preproc)-1:
            infolib.has_type_in_last_pos = True
        
        return infolib
