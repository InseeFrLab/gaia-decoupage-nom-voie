from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.handlers.two_types.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase


def use_case(
    apply_complement_finder=MagicMock(),
    apply_voie_fictive_finder=MagicMock(),
    handle_compl=MagicMock(),
    handle_fictive=MagicMock(),
    handle_has_first=MagicMock(),
    handle_no_first=MagicMock(),
) -> TwoTypesVoiesHandlerUseCase:
    return TwoTypesVoiesHandlerUseCase(
        apply_complement_finder, apply_voie_fictive_finder,
        handle_compl, handle_fictive, handle_has_first, handle_no_first,
    )


def _voie(label: str, nb_types: int = 2, has_type_in_first_pos: bool = True) -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = label.upper().split()
    v.types_and_positions = {("RUE", 1): (0, 0), ("AVENUE", 1): (2, 2)} if nb_types == 2 else {}
    v.has_type_in_first_pos = has_type_in_first_pos
    return v


def test_filtre_voies_a_deux_types():
    # Given — voie avec 1 type filtrée
    voie_1 = _voie("RUE HOCHE", nb_types=1)
    voie_2 = _voie("RUE HOCHE AVENUE VERDIER", nb_types=2)
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([], [voie_2])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([], [voie_2])
    handle_has_mock = MagicMock(); handle_has_mock.execute.return_value = "result"
    # When
    use_case(compl_mock, fictif_mock, handle_has_first=handle_has_mock).execute([voie_1, voie_2])
    # Then — voie_1 ignorée
    handle_has_mock.execute.assert_called_once_with(voie_2)


def test_type_en_premiere_pos_appelle_handle_has():
    # Given
    voie = _voie("RUE HOCHE AVENUE VERDIER", has_type_in_first_pos=True)
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([], [voie])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([], [voie])
    handle_has_mock = MagicMock(); handle_has_mock.execute.return_value = "has_result"
    handle_no_mock = MagicMock()
    # When
    res = use_case(compl_mock, fictif_mock, handle_has_first=handle_has_mock, handle_no_first=handle_no_mock).execute([voie])
    # Then — déterministe : has_type → handle_has, jamais handle_no
    handle_has_mock.execute.assert_called_once_with(voie)
    handle_no_mock.execute.assert_not_called()
    assert res == ["has_result"]


def test_pas_de_type_en_premiere_pos_appelle_handle_no():
    # Given
    voie = _voie("VERDIER RUE HOCHE", has_type_in_first_pos=False)
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([], [voie])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([], [voie])
    handle_has_mock = MagicMock()
    handle_no_mock = MagicMock(); handle_no_mock.execute.return_value = "no_result"
    # When
    res = use_case(compl_mock, fictif_mock, handle_has_first=handle_has_mock, handle_no_first=handle_no_mock).execute([voie])
    # Then — déterministe : pas de type → handle_no, jamais handle_has
    handle_no_mock.execute.assert_called_once_with(voie)
    handle_has_mock.execute.assert_not_called()
    assert res == ["no_result"]


def test_voie_avec_complement_traitee_par_handle_compl():
    # Given
    voie = _voie("RUE HOCHE BAT A")
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([voie], [])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([], [])  # ← manquait
    handle_compl_mock = MagicMock()
    handle_compl_mock.execute.return_value = ("compl_result", None)
    # When
    res = use_case(compl_mock, fictif_mock, handle_compl=handle_compl_mock).execute([voie])
    # Then
    assert "compl_result" in res


def test_voie_fictive_traitee():
    # Given
    voie = _voie("RESIDENCE ERNEST RENAN RUE A")
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([], [voie])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([voie], [])
    handle_fictive_mock = MagicMock(); handle_fictive_mock.execute.return_value = "fictive_result"
    # When
    res = use_case(compl_mock, fictif_mock, handle_fictive=handle_fictive_mock).execute([voie])
    # Then
    assert res == ["fictive_result"]


def test_complement_non_resolu_reinjection_dans_voies():
    # Given — handle_two_types_complement retourne (None, voie_to_treat)
    # → la voie doit être réinjectée dans le flux "voies" pour être traitée
    voie = _voie("RUE HOCHE BAT A")
    voie_reinjected = _voie("RUE HOCHE BAT A", has_type_in_first_pos=True)
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([voie], [])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([], [voie_reinjected])
    handle_compl_mock = MagicMock()
    handle_compl_mock.execute.return_value = (None, voie_reinjected)  # non résolu
    handle_has_mock = MagicMock(); handle_has_mock.execute.return_value = "has_result"
    # When
    res = use_case(compl_mock, fictif_mock, handle_compl=handle_compl_mock,
                   handle_has_first=handle_has_mock).execute([voie])
    # Then — voie_reinjected traitée par handle_has
    handle_has_mock.execute.assert_called()
    assert "has_result" in res


def test_liste_vide():
    # Given
    compl_mock = MagicMock(); compl_mock.execute.return_value = ([], [])
    fictif_mock = MagicMock(); fictif_mock.execute.return_value = ([], [])
    # When
    res = use_case(compl_mock, fictif_mock).execute([])
    # Then
    assert res == []
