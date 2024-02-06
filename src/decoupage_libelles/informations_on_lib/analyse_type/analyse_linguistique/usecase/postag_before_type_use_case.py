from injector import inject

from informations_on_lib.analyse_type.analyse_linguistique.usecase.apply_postagging_use_case import ApplyPostaggingUseCase
from informations_on_lib.analyse_type.analyse_position.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib
from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class PostagBeforeTypeUseCase:
    @inject
    def __init__(self, apply_postagging_use_case: ApplyPostaggingUseCase, order_type_in_lib_use_case: OrderTypeInLib):
         self.apply_postagging_use_case: ApplyPostaggingUseCase = apply_postagging_use_case
         self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infolib: InfoLib, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
            """
            Retourne l'étiquette grammatico-syntaxique du mot précédent
            le type.

            Args:
                type_order (int):
                    Ordre d'apparition du type dans le libellé.
                    1 = 1er, 2 = 2nd...
                    -1 = dernier.

            Returns:
                (str)
            """
            if not infolib.label_postag:
                self.apply_postagging_use_case.execute(infolib)

            if information_on_type_ordered.position_start > 0:
                information_on_type_ordered.postag_before = infolib.label_postag[information_on_type_ordered.position_start-1]
            
            return information_on_type_ordered