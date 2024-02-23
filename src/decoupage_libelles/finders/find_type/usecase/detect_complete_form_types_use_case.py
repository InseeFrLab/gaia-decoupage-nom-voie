from decoupage_libelles.finders.find_type.usecase.list_is_included_in_other_list_use_case import ListIsIncludedInOtherListUseCase
from decoupage_libelles.finders.find_type.usecase.detect_one_word_complete_form_types_use_case import DetectOneWordCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.usecase.detect_multi_words_complete_form_types_use_case import DetectMultiWordsCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class DetectCompleteFormTypesUseCase:
    def __init__(
        self,
        detect_one_word_complete_form_types_use_case: DetectOneWordCompleteFormTypesUseCase = DetectOneWordCompleteFormTypesUseCase(),
        detect_multi_words_complete_form_types_use_case: DetectMultiWordsCompleteFormTypesUseCase = DetectMultiWordsCompleteFormTypesUseCase(),
        list_is_included_in_other_list_use_case: ListIsIncludedInOtherListUseCase = ListIsIncludedInOtherListUseCase(),
    ):
        self.detect_one_word_complete_form_types_use_case: DetectOneWordCompleteFormTypesUseCase = detect_one_word_complete_form_types_use_case
        self.detect_multi_words_complete_form_types_use_case: DetectMultiWordsCompleteFormTypesUseCase = detect_multi_words_complete_form_types_use_case
        self.list_is_included_in_other_list_use_case: ListIsIncludedInOtherListUseCase = list_is_included_in_other_list_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        for type_lib in type_finder_object.type_data.types_lib_preproc:
            type_detect = type_finder_object.type_data.types_lib_preproc2types_lib_raw[type_lib]
            type_detect = type_finder_object.type_data.lib2code[type_detect]
            type_detect = type_finder_object.type_data.code2lib[type_detect]
            nb_words_in_type = len(type_lib.split(" "))

            list_is_included = self.list_is_included_in_other_list_use_case.execute(type_lib.split(" "), type_finder_object.voie_sep)

            # Si le type ne s'écrit qu'en 1 mot
            if type_lib in type_finder_object.voie_sep and nb_words_in_type == 1:
                type_finder_object = self.detect_one_word_complete_form_types_use_case.execute(type_detect, type_lib, type_finder_object)

            # Si le type s'écrit en plusieurs mots
            elif type_lib in type_finder_object.voie and nb_words_in_type > 1 and list_is_included:
                type_finder_object = self.detect_multi_words_complete_form_types_use_case.execute(type_detect, type_lib, type_finder_object)

        return type_finder_object
