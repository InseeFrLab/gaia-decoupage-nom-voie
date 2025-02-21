from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class PositionOfTypesInLibAnalyserUseCase:
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib()):
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie) -> InfoVoie:
        type_ordered_first = self.order_type_in_lib_use_case.execute(infovoie, 1)
        infovoie.has_type_in_first_pos = True if type_ordered_first and type_ordered_first.position_start == 0 else False

        type_ordered_second = self.order_type_in_lib_use_case.execute(infovoie, 2)
        infovoie.has_type_in_second_pos = True if type_ordered_second and type_ordered_second.position_start == 1 else False

        type_ordered_last = self.order_type_in_lib_use_case.execute(infovoie, -1)
        infovoie.has_type_in_last_pos = True if type_ordered_last and type_ordered_last.position_end == len(infovoie.label_preproc) - 1 else False

        return infovoie
