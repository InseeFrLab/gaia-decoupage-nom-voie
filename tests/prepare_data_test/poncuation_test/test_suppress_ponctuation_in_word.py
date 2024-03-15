from decoupage_libelles.prepare_data.ponctuation.usecase.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase


def test_suppression_ponctuation():
    # Given
    chaine_traitee = ["Avenue", "(parentheses"]
    # When
    suppress_ponctuation_in_words_use_case = SuppressPonctuationInWordsUseCase()
    liste_mots = suppress_ponctuation_in_words_use_case.execute(chaine_traitee, ["("])
    # Then
    assert ["Avenue", "parentheses"] == liste_mots


def test_suppression_ponctuation_returns_empty_list():
    # Given
    chaine_traitee = []
    # When
    suppress_ponctuation_in_words_use_case = SuppressPonctuationInWordsUseCase()
    liste_mots = suppress_ponctuation_in_words_use_case.execute(chaine_traitee, ["("])
    # Then
    assert [] == liste_mots
