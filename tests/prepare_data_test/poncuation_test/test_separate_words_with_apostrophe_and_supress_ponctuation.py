from decoupage_libelles.prepare_data.ponctuation.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase


def test_separate_pontuation_and_words_with_apostrophe():
    # Given
    label_to_treat = "HAMEAU L'HERITIER ."
    # When
    separate_words_with_apostrophe_and_supress_ponctuation_use_case = SeparateWordsWithApostropheAndSupressPonctuationUseCase()
    label_treated = separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(label_to_treat, ["."])
    # Then
    label_target = ["HAMEAU", "L", "HERITIER"]
    assert label_target == label_treated


def test_separate_pontuation_and_words_with_apostrophe_returns_empty_list():
    # Given
    label_to_treat = ""
    # When
    separate_words_with_apostrophe_and_supress_ponctuation_use_case = SeparateWordsWithApostropheAndSupressPonctuationUseCase()
    label_treated = separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(label_to_treat, ["."])
    # Then
    label_target = []
    assert label_target == label_treated
