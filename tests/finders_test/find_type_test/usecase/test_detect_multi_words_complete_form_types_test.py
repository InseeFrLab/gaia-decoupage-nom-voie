from unittest.mock import MagicMock
from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.find_positions_of_word_in_sentence_str_use_case import FindPositionsOfWordInSentenceStrUseCase
from decoupage_libelles.finders.find_type.usecase.find_position_of_word_in_sentence_list_use_case import FindPositionOfWordInSentenceListUseCase
from decoupage_libelles.finders.find_type.usecase.detect_multi_words_complete_form_types_use_case import DetectMultiWordsCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


def use_case(
    find_positions_of_word_in_sentence_str_use_case: FindPositionsOfWordInSentenceStrUseCase = MagicMock(),
    find_position_of_word_in_sentence_list_use_case: FindPositionOfWordInSentenceListUseCase = MagicMock(),
) -> DetectMultiWordsCompleteFormTypesUseCase:
    return DetectMultiWordsCompleteFormTypesUseCase(find_positions_of_word_in_sentence_str_use_case, find_position_of_word_in_sentence_list_use_case)


def test_liste_vide():
    # Given
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            code2lib={},
        ),
    )
    type_detect = ""
    type_lib = ""
    find_positions_of_word_in_sentence_str_use_case = MagicMock()
    find_positions_of_word_in_sentence_str_use_case.execute.return_value = []
    # When
    res = use_case(find_positions_of_word_in_sentence_str_use_case, MagicMock()).execute(type_detect, type_lib, type_finder_object)
    # Then
    assert res == type_finder_object


def test_execute():
    # Given
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            code2lib={},
        ),
    )
    type_detect = "type_detect"
    type_lib = ""
    find_positions_of_word_in_sentence_str_use_case = MagicMock()
    find_positions_of_word_in_sentence_str_use_case.execute.return_value = [1, 2, 3]
    find_position_of_word_in_sentence_list_use_case = MagicMock()
    find_position_of_word_in_sentence_list_use_case.execute.return_value = 1
    # When
    res = use_case(find_positions_of_word_in_sentence_str_use_case, find_position_of_word_in_sentence_list_use_case).execute(type_detect, type_lib, type_finder_object)
    # Then
    assert res == type_finder_object
    assert {("type_detect", 1): (1, 1), ("type_detect", 2): (1, 1)} == type_finder_object.voie_big.types_and_positions
