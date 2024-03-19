from decoupage_libelles.finders.find_type.usecase.find_position_of_word_in_sentence_list_use_case import FindPositionOfWordInSentenceListUseCase


def use_case() -> FindPositionOfWordInSentenceListUseCase:
    return FindPositionOfWordInSentenceListUseCase()


def test_execute_start_position():
    # Given
    sentence_list = ["Ceci", "est", "une", "phrase", "de", "test"]
    position_of_first_letter_of_word = 0
    # When
    result = use_case().execute(sentence_list, position_of_first_letter_of_word)
    # Then
    assert result == 0
