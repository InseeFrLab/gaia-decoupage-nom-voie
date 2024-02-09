from injector import inject

from informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_libelle_voie.model.infovoie import InfoVoie
from informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class HasTypeInMiddlePositionUseCase:
    @inject
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib):
         self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
        type_ordered_middle = self.order_type_in_lib_use_case.execute(infovoie, information_on_type_ordered.order_in_lib)
        if type_ordered_middle:
            if (information_on_type_ordered.order_in_lib-1 < type_ordered_middle.position_start and
                    not type_ordered_middle.position_start==len(infovoie.label_preproc)-1):
                information_on_type_ordered.is_in_middle_position = True
        
        return information_on_type_ordered
