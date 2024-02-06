from injector import inject

from informations_on_lib.analyse_type.analyse_position.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib
from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class HasTypeInMiddlePositionUseCase:
    @inject
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib):
         self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infolib: InfoLib, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
        type_ordered_middle = self.order_type_in_lib_use_case.execute(infolib, information_on_type_ordered.order_in_lib)
        if type_ordered_middle:
            if (information_on_type_ordered.order_in_lib-1 < type_ordered_middle.position_start and
                    not type_ordered_middle.position_start==len(infolib.label_preproc)-1):
                information_on_type_ordered.is_in_middle_position = True
        
        return information_on_type_ordered
