from decoupage_libelles.finders.find_type.usecase.detect_codified_types_use_case import DetectCodifiedTypesUseCase
from decoupage_libelles.finders.find_type.usecase.detect_complete_form_types_use_case import DetectCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.usecase.update_occurences_by_order_of_apparition_use_case import UpdateOccurencesByOrderOfApparitionUseCase
from decoupage_libelles.finders.find_type.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase
from decoupage_libelles.finders.find_type.usecase.remove_wrong_detected_codes_use_case import RemoveWrongDetectedCodesUseCase
from decoupage_libelles.finders.find_type.usecase.remove_wrong_types_in_lib_use_case import RemoveWrongTypesInLibUseCase
from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class TypeFinderUseCase:
    def __init__(
        self,
        detect_codified_types_use_case: DetectCodifiedTypesUseCase = DetectCodifiedTypesUseCase(),
        detect_complete_form_types_use_case: DetectCompleteFormTypesUseCase = DetectCompleteFormTypesUseCase(),
        update_occurences_by_order_of_apparition_use_case: UpdateOccurencesByOrderOfApparitionUseCase = UpdateOccurencesByOrderOfApparitionUseCase(),
        remove_duplicates_use_case: RemoveDuplicatesUseCase = RemoveDuplicatesUseCase(),
        remove_wrong_detected_codes_use_case: RemoveWrongDetectedCodesUseCase = RemoveWrongDetectedCodesUseCase(),
        remove_wrong_types_in_lib_use_case: RemoveWrongTypesInLibUseCase = RemoveWrongTypesInLibUseCase(),
    ):
        self.detect_codified_types_use_case: DetectCodifiedTypesUseCase = detect_codified_types_use_case
        self.detect_complete_form_types_use_case: DetectCompleteFormTypesUseCase = detect_complete_form_types_use_case
        self.update_occurences_by_order_of_apparition_use_case: UpdateOccurencesByOrderOfApparitionUseCase = update_occurences_by_order_of_apparition_use_case
        self.remove_duplicates_use_case: RemoveDuplicatesUseCase = remove_duplicates_use_case
        self.remove_wrong_detected_codes_use_case: RemoveWrongDetectedCodesUseCase = remove_wrong_detected_codes_use_case
        self.remove_wrong_types_in_lib_use_case: RemoveWrongTypesInLibUseCase = remove_wrong_types_in_lib_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> InfoVoie:
        type_finder_object.voie_sep = type_finder_object.voie_big.label_preproc[:]
        type_finder_object.voie = (" ").join(type_finder_object.voie_big.label_preproc[:])
        type_finder_object = self.detect_codified_types_use_case.execute(type_finder_object)
        type_finder_object = self.detect_complete_form_types_use_case.execute(type_finder_object)
        types_detected = [type_lib for type_lib, __ in type_finder_object.voie_big.types_and_positions.keys()]
        if len(types_detected) > 1:
            self.update_occurences_by_order_of_apparition_use_case.execute(type_finder_object)
            self.remove_duplicates_use_case.execute(type_finder_object)
            self.remove_wrong_detected_codes_use_case.execute(type_finder_object)
            self.remove_wrong_types_in_lib_use_case.execute(type_finder_object)
        return type_finder_object.voie_big
