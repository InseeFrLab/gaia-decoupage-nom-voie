from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase


def test_execute_with_position_end():
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three", "four", "five"])
    position_start = 1
    position_end = 4
    # When
    result = GetWordsBetweenUseCase().execute(infovoie, position_start, position_end)
    # Then
    assert result == "two three four"


def test_execute_without_position_end():
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three", "four", "five"])
    position_start = 2
    # When
    result = GetWordsBetweenUseCase().execute(infovoie, position_start)
    # Then
    assert result == "three four five"


def test_execute_with_position_end_out_of_bounds():
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three", "four", "five"])
    position_start = 2
    position_end = 10
    # When
    result = GetWordsBetweenUseCase().execute(infovoie, position_start, position_end)
    # Then
    assert result is None
