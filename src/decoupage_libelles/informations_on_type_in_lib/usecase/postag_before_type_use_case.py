from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class PostagBeforeTypeUseCase:
    POSTAG = ["DET", "ADJ", "ADP", "CCONJ"]

    def __init__(
        self,
        order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib(),
    ):
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
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
        if information_on_type_ordered.position_start > 0 and infovoie.label_postag:
            postag = infovoie.label_postag[information_on_type_ordered.position_start - 1]
            information_on_type_ordered.postag_before = postag

            information_on_type_ordered.has_adj_det_before = (
                True if postag in PostagBeforeTypeUseCase.POSTAG and information_on_type_ordered.word_before != "A" or information_on_type_ordered.word_before in ["DIT", "DITE"] else False
            )

        return information_on_type_ordered
