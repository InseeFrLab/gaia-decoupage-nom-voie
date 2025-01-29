from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.find_positions_of_word_in_sentence_str_use_case import FindPositionsOfWordInSentenceStrUseCase
from decoupage_libelles.finders.find_type.usecase.find_position_of_word_in_sentence_list_use_case import FindPositionOfWordInSentenceListUseCase


class DetectMultiWordsCompleteFormTypesUseCase:
    def __init__(
        self,
        find_positions_of_word_in_sentence_str_use_case: FindPositionsOfWordInSentenceStrUseCase = FindPositionsOfWordInSentenceStrUseCase(),
        find_position_of_word_in_sentence_list_use_case: FindPositionOfWordInSentenceListUseCase = FindPositionOfWordInSentenceListUseCase(),
    ):
        self.find_positions_of_word_in_sentence_str_use_case: FindPositionsOfWordInSentenceStrUseCase = find_positions_of_word_in_sentence_str_use_case
        self.find_position_of_word_in_sentence_list_use_case: FindPositionOfWordInSentenceListUseCase = find_position_of_word_in_sentence_list_use_case

    def execute(self, type_detect: str, type_lib: str, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        nb_words_in_type = len(type_lib.split(" "))
        pos_debut = self.find_positions_of_word_in_sentence_str_use_case.execute(type_finder_object.voie, type_lib)
        for pos in pos_debut:
            pos_type = self.find_position_of_word_in_sentence_list_use_case.execute(type_finder_object.voie_sep, pos)
            types_detected = [type_lib for type_lib, __ in type_finder_object.voie_big.types_and_positions.keys()]
            position_index = 1 if type_detect not in types_detected else 2
            if pos_type is not None:
                type_finder_object.voie_big.types_and_positions[(type_detect, position_index)] = (pos_type, pos_type + nb_words_in_type - 1)
        return type_finder_object
