from decoupage_libelles.informations_on_type_in_lib.usecase.postag_before_type_use_case import PostagBeforeTypeUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.word_after_type_use_case import WordAfterTypeUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.word_before_type_use_case import WordBeforeTypeUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_type_in_lib.usecase.is_in_middle_pos_use_case import IsInMiddlePositionUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.is_in_penultimate_position_use_case import IsInPenultimatePositionUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.type_is_longitudinal_or_agglomerant_use_case import TypeIsLongitudinalOrAgglomerantUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.type_is_complementaire_use_case import TypeIsComplementaireUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.type_after_type_use_case import TypeAfterTypeUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.informations_on_type_in_lib.usecase.find_order_of_apparition_in_lib_use_case import FindOrderOfApparitionInLibUseCase


class GenerateInformationOnTypeOrderedUseCase:
    def __init__(
        self,
        postag_before_type_use_case: PostagBeforeTypeUseCase = PostagBeforeTypeUseCase(),
        word_after_type_use_case: WordAfterTypeUseCase = WordAfterTypeUseCase(),
        word_before_type_use_case: WordBeforeTypeUseCase = WordBeforeTypeUseCase(),
        order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib(),
        is_in_middle_pos_use_case: IsInMiddlePositionUseCase = IsInMiddlePositionUseCase(),
        is_in_penultimate_position_use_case: IsInPenultimatePositionUseCase = IsInPenultimatePositionUseCase(),
        type_is_longitudinal_or_agglomerant_use_case: TypeIsLongitudinalOrAgglomerantUseCase = TypeIsLongitudinalOrAgglomerantUseCase(),
        type_is_complementaire_use_case: TypeIsComplementaireUseCase = TypeIsComplementaireUseCase(),
        type_after_type_use_case: TypeAfterTypeUseCase = TypeAfterTypeUseCase(),
        find_order_of_apparition_in_lib_use_case: FindOrderOfApparitionInLibUseCase = FindOrderOfApparitionInLibUseCase(),
    ):
        self.postag_before_type_use_case: PostagBeforeTypeUseCase = postag_before_type_use_case
        self.word_after_type_use_case: WordAfterTypeUseCase = word_after_type_use_case
        self.word_before_type_use_case: WordBeforeTypeUseCase = word_before_type_use_case
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case
        self.is_in_middle_pos_use_case: IsInMiddlePositionUseCase = is_in_middle_pos_use_case
        self.is_in_penultimate_position_use_case: IsInPenultimatePositionUseCase = is_in_penultimate_position_use_case
        self.type_is_longitudinal_or_agglomerant_use_case: TypeIsLongitudinalOrAgglomerantUseCase = type_is_longitudinal_or_agglomerant_use_case
        self.type_is_complementaire_use_case: TypeIsComplementaireUseCase = type_is_complementaire_use_case
        self.type_after_type_use_case: TypeAfterTypeUseCase = type_after_type_use_case
        self.find_order_of_apparition_in_lib_use_case: FindOrderOfApparitionInLibUseCase = find_order_of_apparition_in_lib_use_case

    def execute(self, infovoie: InfoVoie, type_order: int, type_name: str = None, occurence: int = None) -> InformationOnTypeOrdered:
        if type_order:
            type_ordered = self.order_type_in_lib_use_case.execute(infovoie=infovoie, type_order=type_order)
        elif type_name and occurence:
            type_ordered = self.find_order_of_apparition_in_lib_use_case.execute(infovoie=infovoie, type_name=type_name, occurence=occurence)
        else:
            type_ordered = None
        if type_ordered:
            self.word_after_type_use_case.execute(infovoie, type_ordered)
            self.word_before_type_use_case.execute(infovoie, type_ordered)
            self.is_in_middle_pos_use_case.execute(infovoie, type_ordered)
            self.is_in_penultimate_position_use_case.execute(infovoie, type_ordered)
            self.type_is_longitudinal_or_agglomerant_use_case.execute(infovoie, type_ordered)
            self.type_is_complementaire_use_case.execute(infovoie, type_ordered)
            self.postag_before_type_use_case.execute(infovoie, type_ordered)
            self.type_after_type_use_case.execute(infovoie, type_ordered)

            return type_ordered
