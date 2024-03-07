from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class WordBeforeTypeUseCase:
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib()):
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered):
        type_ordered = self.order_type_in_lib_use_case.execute(infovoie, information_on_type_ordered.order_in_lib)
        if type_ordered and type_ordered.position_start > 0:
            index_word_before = type_ordered.position_start - 1
            information_on_type_ordered.word_before = infovoie.label_preproc[index_word_before]

        return information_on_type_ordered
