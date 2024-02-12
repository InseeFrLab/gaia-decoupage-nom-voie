from injector import inject

from informations_on_type_in_lib.domain.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_type_in_lib.domain.model.information_on_type_ordered import InformationOnTypeOrdered


class IsInPenultimatePositionUseCase:
    @inject
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib):
         self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
        type_ordered_penultimate = self.order_type_in_lib_use_case.execute(infovoie, information_on_type_ordered.order_in_lib)
        if type_ordered_penultimate:
            if type_ordered_penultimate.position_end == len(infovoie.label_preproc)-2:
                information_on_type_ordered.is_in_penultimate_position = True
            
        return information_on_type_ordered
