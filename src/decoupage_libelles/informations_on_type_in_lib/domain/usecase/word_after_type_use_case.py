from injector import inject

from informations_on_type_in_lib.domain.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_type_in_lib.domain.model.information_on_type_ordered import InformationOnTypeOrdered


class WordAfterTypeUseCase:
    @inject
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib):
         self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered):
        position_type_in_lib_end = information_on_type_ordered.position_end
        if (position_type_in_lib_end or
                not position_type_in_lib_end == len(infovoie.label_preproc)-1):
            index_word_after = position_type_in_lib_end + 1
            information_on_type_ordered.word_after = infovoie.label_preproc[index_word_after]
        
        return information_on_type_ordered
