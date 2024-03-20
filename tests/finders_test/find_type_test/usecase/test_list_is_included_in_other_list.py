from decoupage_libelles.finders.find_type.usecase.list_is_included_in_other_list_use_case import ListIsIncludedInOtherListUseCase


def use_case() -> ListIsIncludedInOtherListUseCase:
    return ListIsIncludedInOtherListUseCase()


def test_execute_retourne_false_si_petite_liste_vide():
    # Given
    petite_liste = []
    grande_liste = ["a", "b", "c"]
    # When
    res: bool = use_case().execute(petite_liste, grande_liste)
    # Then
    assert not res


def test_execute_retourne_false_si_petite_liste_non_presente_dans_grande_liste():
    # Given
    petite_liste = ["x", "y"]
    grande_liste = ["a", "b", "c"]
    # When
    res: bool = use_case().execute(petite_liste, grande_liste)
    # Then
    assert not res


def test_execute_retourne_true_si_petite_liste_presente_dans_grande_liste():
    # Given
    petite_liste = ["b", "c"]
    grande_liste = ["a", "b", "c", "d", "e"]
    # When
    res: bool = use_case().execute(petite_liste, grande_liste)
    # Then
    assert res


def test_execute_retourne_false_si_petite_liste_plus_longue_que_grande_liste():
    # Given
    petite_liste = ["a", "b", "c", "d", "e"]
    grande_liste = ["a", "b", "c"]
    # When
    res: bool = use_case().execute(petite_liste, grande_liste)
    # Then
    assert not res


def test_execute_retourne_true_si_petite_liste_egale_a_grande_liste():
    # Given
    petite_liste = ["a", "b", "c"]
    grande_liste = ["a", "b", "c"]
    # When
    res: bool = use_case().execute(petite_liste, grande_liste)
    # Then
    assert res
