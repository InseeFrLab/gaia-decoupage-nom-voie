from decoupage_libelles.finders.find_type.usecase.list_is_included import list_is_included


def test_inclus_au_debut():
    # Given
    sub = ["A", "B"]
    full = ["A", "B", "C"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is True


def test_inclus_au_milieu():
    # Given
    sub = ["B", "C"]
    full = ["A", "B", "C", "D"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is True


def test_inclus_a_la_fin():
    # Given
    sub = ["C", "D"]
    full = ["A", "B", "C", "D"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is True


def test_non_inclus():
    # Given
    sub = ["X", "Y"]
    full = ["A", "B", "C"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is False


def test_sous_liste_vide():
    # Given
    sub = []
    full = ["A", "B"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is False


def test_sous_liste_plus_grande_que_full():
    # Given
    sub = ["A", "B", "C"]
    full = ["A", "B"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is False


def test_ordre_compte():
    # Given
    sub = ["B", "A"]
    full = ["A", "B", "C"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is False


def test_listes_egales():
    # Given
    sub = ["A", "B"]
    full = ["A", "B"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is True


def test_un_seul_element_present():
    # Given
    sub = ["B"]
    full = ["A", "B", "C"]
    # When
    res = list_is_included(sub, full)
    # Then
    assert res is True
