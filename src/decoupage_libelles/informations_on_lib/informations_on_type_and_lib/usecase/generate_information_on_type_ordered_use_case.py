from injector import inject

from informations_on_lib.analyse_type.analyse_linguistique.usecase.postag_before_type_use_case import PostagBeforeTypeUseCase
from informations_on_lib.analyse_type.analyse_linguistique.usecase.has_adj_det_before_type_use_case import HasAdjDetBeforeTypeUseCase
from informations_on_lib.analyse_type.analyse_linguistique.usecase.word_after_type_use_case import WordAfterTypeUseCase
from informations_on_lib.analyse_type.analyse_linguistique.usecase.word_before_type_use_case import WordBeforeTypeUseCase
from informations_on_lib.analyse_type.analyse_position.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_lib.analyse_type.analyse_position.usecase.has_type_in_middle_pos_use_case import HasTypeInMiddlePositionUseCase
from informations_on_lib.analyse_type.analyse_position.usecase.has_type_in_penultimate_position_use_case import HasTypeInPenultimatePositionUseCase
from informations_on_lib.analyse_type.analyse_sort_of_type.usecase.type_is_agglomerant_use_case import TypeIsAgglomerantUseCase
from informations_on_lib.analyse_type.analyse_sort_of_type.usecase.type_is_longitudinal_use_case import TypeIsLongitudinalUseCase
from informations_on_lib.analyse_type.analyse_sort_of_type.usecase.type_is_complementaire_use_case import TypeIsComplementaireUseCase
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib
from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered

class GenerateInformationOnTypeOrderedUseCase:
    @inject
    def __init__(self, postag_before_type_use_case: PostagBeforeTypeUseCase,
                 has_adj_det_before_type_use_case: HasAdjDetBeforeTypeUseCase,
                 word_after_type_use_case: WordAfterTypeUseCase,
                 word_before_type_use_case: WordBeforeTypeUseCase,
                 order_type_in_lib_use_case: OrderTypeInLib,
                 has_type_in_middle_pos_use_case: HasTypeInMiddlePositionUseCase,
                 has_type_in_penultimate_position_use_case: HasTypeInPenultimatePositionUseCase,
                 type_is_agglomerant_use_case: TypeIsAgglomerantUseCase,
                 type_is_longitudinal_use_case: TypeIsLongitudinalUseCase,
                 type_is_complementaire_use_case: TypeIsComplementaireUseCase):
        self.postag_before_type_use_case: PostagBeforeTypeUseCase = postag_before_type_use_case
        self.has_adj_det_before_type_use_case: HasAdjDetBeforeTypeUseCase = has_adj_det_before_type_use_case
        self.word_after_type_use_case: WordAfterTypeUseCase = word_after_type_use_case
        self.word_before_type_use_case: WordBeforeTypeUseCase = word_before_type_use_case
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case
        self.has_type_in_middle_pos_use_case: HasTypeInMiddlePositionUseCase = has_type_in_middle_pos_use_case
        self.has_type_in_penultimate_position_use_case: HasTypeInPenultimatePositionUseCase = has_type_in_penultimate_position_use_case
        self.type_is_agglomerant_use_case: TypeIsAgglomerantUseCase = type_is_agglomerant_use_case
        self.type_is_longitudinal_use_case: TypeIsLongitudinalUseCase = type_is_longitudinal_use_case
        self.type_is_complementaire_use_case: TypeIsComplementaireUseCase = type_is_complementaire_use_case

    def execute(self, infolib: InfoLib, type_order: int, apply_nlp_model: bool = False) -> InformationOnTypeOrdered:
        type_ordered = self.order_type_in_lib_use_case.execute(infolib=infolib, type_order=type_order)
        if type_ordered:
            self.word_after_type_use_case.execute(infolib, type_ordered)
            self.word_before_type_use_case.execute(infolib, type_ordered)
            self.has_type_in_middle_pos_use_case.execute(infolib, type_ordered)
            self.has_type_in_penultimate_position_use_case.execute(infolib, type_ordered)
            self.type_is_agglomerant_use_case.execute(type_ordered)
            self.type_is_longitudinal_use_case.execute(infolib, type_ordered)
            self.type_is_complementaire_use_case.execute(infolib, type_ordered)
            self.postag_before_type_use_case.execute(infolib, type_ordered)
            self.has_adj_det_before_type_use_case.execute(type_ordered)
