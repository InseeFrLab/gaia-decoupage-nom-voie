from decoupage_libelles.finders.find_type.usecase.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case import DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase


def use_case() -> DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase:
    return DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase()


def test_execute():
    # Given
    str1 = "Ceci est une phrase."
    str2 = "Voici une autre phrase."
    # When
    result = use_case().execute(str1, str2)
    # Then
    assert result == ("Ceci est une phrase.", "Voici une autre phrase.")


def test_execute_str1_longer():
    # Given
    str1 = "Ceci est une phrase plus longue."
    str2 = "Autre phrase."
    # When
    result = use_case().execute(str1, str2)
    # Then
    assert result == ("Autre phrase.", "Ceci est une phrase plus longue.")


def test_execute_str2_longer():
    # Given
    str1 = "Courte phrase."
    str2 = "Voici une phrase plus longue."
    # When
    result = use_case().execute(str1, str2)
    # Then
    assert result == ("Courte phrase.", "Voici une phrase plus longue.")
