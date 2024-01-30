from injector import inject

from voie_classes.voie import Voie
from utils.utils_for_lists import list_incluse
from finders.find_type.domain.usecase.generate_type_finder_utils_use_case import TypeFinderUtils
from voie_classes.informations_on_libelle import InfoLib
from finders.find_type.domain.usecase.detect_one_word_complete_form_types_use_case import DetectOneWordCompleteFormTypesUseCase
from finders.find_type.domain.usecase.detect_multi_words_complete_form_types_use_case import DetectMultiWordsCompleteFormTypesUseCase
from finders.find_type.domain.model.type_finder_object import TypeFinderObject


class DetectCompleteFormTypesUseCase():
    @inject
    def __init__(self,
                 detect_one_word_complete_form_types_use_case: DetectOneWordCompleteFormTypesUseCase,
                 detect_multi_words_complete_form_types_use_case: DetectMultiWordsCompleteFormTypesUseCase
                 ):
        self.detect_one_word_complete_form_types_use_case: DetectOneWordCompleteFormTypesUseCase = detect_one_word_complete_form_types_use_case
        self.detect_multi_words_complete_form_types_use_case: DetectMultiWordsCompleteFormTypesUseCase = detect_multi_words_complete_form_types_use_case

    def execute(self,
                type_finder_object: TypeFinderObject) -> TypeFinderObject:

        for type_lib in type_finder_object.type_data.types_lib_preproc:
            type_detect = type_finder_object.type_data.types_lib_preproc2types_lib_raw[type_lib]
            type_detect = type_finder_object.type_data.lib2code[type_detect]
            type_detect = type_finder_object.type_data.code2lib[type_detect]
            nb_words_in_type = len(type_lib.split(' '))

            # Si le type ne s'écrit qu'en 1 mot
            if type_lib in type_finder_object.voie_sep and nb_words_in_type == 1:
                type_finder_object = self.detect_one_word_complete_form_types_use_case.execute(
                            type_detect, type_lib, type_finder_object)

            # Si le type s'écrit en plusieurs mots
            elif (type_lib in type_finder_object.voie and
                  nb_words_in_type > 1 and
                  list_incluse(type_lib.split(' '), type_finder_object.voie_sep)):
                type_finder_object = self.detect_multi_words_complete_form_types_use_case.execute(
                            type_detect, type_lib, type_finder_object)

        return type_finder_object