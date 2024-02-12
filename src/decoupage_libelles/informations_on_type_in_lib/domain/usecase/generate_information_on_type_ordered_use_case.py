from injector import inject

from informations_on_type_in_lib.domain.usecase.postag_before_type_use_case import PostagBeforeTypeUseCase
from informations_on_type_in_lib.domain.usecase.word_after_type_use_case import WordAfterTypeUseCase
from informations_on_type_in_lib.domain.usecase.word_before_type_use_case import WordBeforeTypeUseCase
from informations_on_type_in_lib.domain.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_type_in_lib.domain.usecase.is_in_middle_pos_use_case import IsInMiddlePositionUseCase
from informations_on_type_in_lib.domain.usecase.is_in_penultimate_position_use_case import IsInPenultimatePositionUseCase
from informations_on_type_in_lib.domain.usecase.type_is_agglomerant_use_case import TypeIsAgglomerantUseCase
from informations_on_type_in_lib.domain.usecase.type_is_longitudinal_use_case import TypeIsLongitudinalUseCase
from informations_on_type_in_lib.domain.usecase.type_is_complementaire_use_case import TypeIsComplementaireUseCase
from informations_on_type_in_lib.domain.usecase.type_after_type_use_case import TypeAfterTypeUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_type_in_lib.domain.model.information_on_type_ordered import InformationOnTypeOrdered
from informations_on_type_in_lib.domain.usecase.find_order_of_apparition_in_lib_use_case import FindOrderOfApparitionInLibUseCase


class GenerateInformationOnTypeOrderedUseCase:
    @inject
    def __init__(self, postag_before_type_use_case: PostagBeforeTypeUseCase,
                 word_after_type_use_case: WordAfterTypeUseCase,
                 word_before_type_use_case: WordBeforeTypeUseCase,
                 order_type_in_lib_use_case: OrderTypeInLib,
                 is_in_middle_pos_use_case: IsInMiddlePositionUseCase,
                 is_in_penultimate_position_use_case: IsInPenultimatePositionUseCase,
                 type_is_agglomerant_use_case: TypeIsAgglomerantUseCase,
                 type_is_longitudinal_use_case: TypeIsLongitudinalUseCase,
                 type_is_complementaire_use_case: TypeIsComplementaireUseCase,
                 type_after_type_use_case: TypeAfterTypeUseCase,
                 find_order_of_apparition_in_lib_use_case: FindOrderOfApparitionInLibUseCase):
        self.postag_before_type_use_case: PostagBeforeTypeUseCase = postag_before_type_use_case
        self.word_after_type_use_case: WordAfterTypeUseCase = word_after_type_use_case
        self.word_before_type_use_case: WordBeforeTypeUseCase = word_before_type_use_case
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case
        self.is_in_middle_pos_use_case: IsInMiddlePositionUseCase = has_type_in_middle_pos_use_case
        self.is_in_penultimate_position_use_case: IsInPenultimatePositionUseCase = has_type_in_penultimate_position_use_case
        self.type_is_agglomerant_use_case: TypeIsAgglomerantUseCase = type_is_agglomerant_use_case
        self.type_is_longitudinal_use_case: TypeIsLongitudinalUseCase = type_is_longitudinal_use_case
        self.type_is_complementaire_use_case: TypeIsComplementaireUseCase = type_is_complementaire_use_case
        self.type_after_type_use_case: TypeAfterTypeUseCase = type_after_type_use_case
        self.find_order_of_apparition_in_lib_use_case: FindOrderOfApparitionInLibUseCase = find_order_of_apparition_in_lib_use_case

    def execute(self, infovoie: InfoVoie, type_order: int, type_name: str = None, occurence: int = None) -> InformationOnTypeOrdered:
        if type_order:
            type_ordered = self.order_type_in_lib_use_case.execute(infovoie=infovoie, type_order=type_order)
        else:
            type_ordered = self.find_order_of_apparition_in_lib_use_case.execute(type_name=type_name, occurence=occurence)
        if type_ordered:
            self.word_after_type_use_case.execute(infovoie, type_ordered)
            self.word_before_type_use_case.execute(infovoie, type_ordered)
            self.is_in_middle_pos_use_case.execute(infovoie, type_ordered)
            self.is_in_penultimate_position_use_case.execute(infovoie, type_ordered)
            self.type_is_agglomerant_use_case.execute(type_ordered)
            self.type_is_longitudinal_use_case.execute(infovoie, type_ordered)
            self.type_is_complementaire_use_case.execute(infovoie, type_ordered)
            self.postag_before_type_use_case.execute(infovoie, type_ordered)
            self.type_after_type_use_case.execute(infovoie, type_ordered)

        return type_ordered