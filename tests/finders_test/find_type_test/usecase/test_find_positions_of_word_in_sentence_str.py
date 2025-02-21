from decoupage_libelles.finders.find_type.usecase.find_positions_of_word_in_sentence_str_use_case import FindPositionsOfWordInSentenceStrUseCase


def use_case() -> FindPositionsOfWordInSentenceStrUseCase:
    return FindPositionsOfWordInSentenceStrUseCase()


def test_execute_single_occurrence():
    # Given
    sentence = "Ceci est une phrase de test."
    word_to_find = "phrase"
    # When
    result = use_case().execute(sentence, word_to_find)
    # Then
    assert result == [13]


def test_execute_multiple_occurrences():
    # Given
    sentence = "Ceci est une phrase de test et une autre phrase de test."
    word_to_find = "phrase"
    # When
    result = use_case().execute(sentence, word_to_find)
    # Then
    assert result == [13, 41]


def test_execute_word_not_found():
    # Given
    sentence = "Ceci est une phrase de test."
    word_to_find = "inexistant"
    # When
    result = use_case().execute(sentence, word_to_find)
    # Then
    assert result == []
