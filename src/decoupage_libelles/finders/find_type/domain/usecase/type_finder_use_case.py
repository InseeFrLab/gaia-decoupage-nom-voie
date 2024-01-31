from injector import inject

from finders.find_type.domain.usecase.detect_codified_types_use_case import DetectCodifiedTypesUseCase
from finders.find_type.domain.usecase.detect_complete_form_types_use_case import DetectCompleteFormTypesUseCase
from finders.find_type.domain.usecase.update_occurences_by_order_of_apparition_use_case import UpdateOccurencesByOrderOfApparitionUseCase
from finders.find_type.domain.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase
from finders.find_type.domain.usecase.remove_wrong_detected_codes_use_case import RemoveWrongDetectedCodesUseCase
from finders.find_type.domain.model.type_finder_object import TypeFinderObject
from voie_classes.voie import Voie

class TypeFinder:
    @inject
    def __init__(self,
                 detect_codified_types_use_case: DetectCodifiedTypesUseCase,
                 detect_complete_form_types_use_case: DetectCompleteFormTypesUseCase,
                 update_occurences_by_order_of_apparition_use_case: UpdateOccurencesByOrderOfApparitionUseCase,
                 remove_duplicates_use_case: RemoveDuplicatesUseCase,
                 remove_wrong_detected_codes_use_case: RemoveWrongDetectedCodesUseCase):
        self.detect_codified_types_use_case: DetectCodifiedTypesUseCase = detect_codified_types_use_case
        self.detect_complete_form_types_use_case: DetectCompleteFormTypesUseCase = detect_complete_form_types_use_case
        self.update_occurences_by_order_of_apparition_use_case: UpdateOccurencesByOrderOfApparitionUseCase = update_occurences_by_order_of_apparition_use_case
        self.remove_duplicates_use_case: RemoveDuplicatesUseCase = remove_duplicates_use_case
        self.remove_wrong_detected_codes_use_case: RemoveWrongDetectedCodesUseCase = remove_wrong_detected_codes_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> Voie:
        self.detect_codified_types_use_case.execute(type_finder_object)
        self.detect_complete_form_types_use_case.execute(type_finder_object)
        if type_finder_object.infolib.nb_types_detected() > 1:
            self.update_occurences_by_order_of_apparition_use_case.execute(type_finder_object)
            self.remove_duplicates_use_case.execute(type_finder_object)
            self.remove_wrong_detected_codes_use_case.execute(type_finder_object)
        type_finder_object.voie_big.infolib = type_finder_object.infolib
        return type_finder_object.voie_big