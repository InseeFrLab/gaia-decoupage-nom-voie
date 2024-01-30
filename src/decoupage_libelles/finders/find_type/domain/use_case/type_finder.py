from injector import inject

from finders.find_type.domain.use_case.detect_codified_types import DetectCodifiedTypes
from finders.find_type.domain.use_case.detect_complete_form_types.detect_complete_form_types import DetectCompleteFormTypes
from finders.find_type.domain.use_case.update_occurences_by_order_of_apparition import UpdateOccurencesByOrderOfApparition
from finders.find_type.domain.use_case.remove_duplicates import RemoveDuplicates
from finders.find_type.domain.use_case.remove_wrong_detected_codes import RemoveWrongDetectedCodes
from finders.find_type.domain.model.type_finder_object import TypeFinderObject

class TypeFinder:
    @inject
    def __init__(self,
                 detect_codified_types: DetectCodifiedTypes,
                 detect_complete_form_types: DetectCompleteFormTypes,
                 update_occurences_by_order_of_apparition: UpdateOccurencesByOrderOfApparition,
                 remove_duplicates: RemoveDuplicates,
                 remove_wrong_detected_codes: RemoveWrongDetectedCodes):
        self.detect_codified_types: DetectCodifiedTypes = detect_codified_types
        self.detect_complete_form_types: DetectCompleteFormTypes = detect_complete_form_types
        self.update_occurences_by_order_of_apparition: UpdateOccurencesByOrderOfApparition = update_occurences_by_order_of_apparition
        self.remove_duplicates: RemoveDuplicates = remove_duplicates
        self.remove_wrong_detected_codes: RemoveWrongDetectedCodes = remove_wrong_detected_codes

    def execute(self, type_finder_object: TypeFinderObject):
        self.detect_codified_types.execute(type_finder_object)
        self.detect_complete_form_types.execute(type_finder_object)
        if type_finder_object.infolib.nb_types_detected() > 1:
            self.update_occurences_by_order_of_apparition.execute(type_finder_object)
            self.remove_duplicates.execute(type_finder_object)
            self.remove_wrong_detected_codes.execute(type_finder_object)
        type_finder_object.voie_big.infolib = type_finder_object.infolib
        return type_finder_object.voie_big