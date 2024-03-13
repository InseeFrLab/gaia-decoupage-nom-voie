from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class WordAfterTypeUseCase:
    def __init__(
        self,
        order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib(),
    ):
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered):
        position_type_in_lib_end = information_on_type_ordered.position_end
        if position_type_in_lib_end or not position_type_in_lib_end == len(infovoie.label_preproc) - 1:
            index_word_after = position_type_in_lib_end + 1
            information_on_type_ordered.word_after = infovoie.label_preproc[index_word_after]

        return information_on_type_ordered
