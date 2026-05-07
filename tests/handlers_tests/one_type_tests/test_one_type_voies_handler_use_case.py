from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.handlers.one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase


def use_case(
    apply_complement_finder=MagicMock(),
    apply_voie_fictive_finder=MagicMock(),
    handle_compl=MagicMock(),
    handle_not_compl_not_fictif=MagicMock(),
    assign_lib_compl=MagicMock(),
    gen_info_lib=MagicMock(),
    suppress_article=MagicMock(),
) -> OneTypeVoiesHandlerUseCase:
    return OneTypeVoiesHandlerUseCase(
        apply_complement_finder, apply_voie_fictive_finder,
        handle_compl, handle_not_compl_not_fictif,
        assign_lib_compl, gen_info_lib, suppress_article,
    )


def _voie(label: str, nb_types: int = 1) -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = label.upper().split()
    v.types_and_positions = {("RUE", 1): (0, 0)} if nb_types == 1 else {}
    return v


def test_filtre_voies_a_un_seul_type():
    # Given — une voie avec 0 type doit être filtrée
    voie_0 = _voie("LES LILAS", nb_types=0)
    voie_1 = _voie("RUE HOCHE", nb_types=1)
    compl_mock = MagicMock()
    compl_mock.execute.return_value = ([], [voie_1])
    fictif_mock = MagicMock()
    fictif_mock.execute.return_value = ([], [voie_1])
    not_compl_mock = MagicMock()
    not_compl_mock.execute.return_value = "lib_result"
    # When
    res = use_case(compl_mock, fictif_mock, handle_not_compl_not_fictif=not_compl_mock).execute([voie_0, voie_1])
    # Then — voie_0 ignorée, voie_1 traitée
    not_compl_mock.execute.assert_called_once_with(voie_1)
    assert res == ["lib_result"]


def test_pretraitement_applique_avant_complement():
    # Given
    voie = _voie("CHE DES SEMAPHORES")
    suppress_mock = MagicMock()
    suppress_mock.execute.side_effect = lambda v: v
    gen_info_mock = MagicMock()
    gen_info_mock.execute.side_effect = lambda v, **kw: v
    compl_mock = MagicMock()
    compl_mock.execute.return_value = ([], [voie])
    fictif_mock = MagicMock()
    fictif_mock.execute.return_value = ([], [voie])
    not_compl_mock = MagicMock()
    not_compl_mock.execute.return_value = "result"
    # When
    use_case(compl_mock, fictif_mock, handle_not_compl_not_fictif=not_compl_mock,
             gen_info_lib=gen_info_mock, suppress_article=suppress_mock).execute([voie])
    # Then — suppress + gen_info appelés avant la recherche de complément
    suppress_mock.execute.assert_called_once()
    gen_info_mock.execute.assert_called()


def test_voie_avec_complement():
    # Given
    voie = _voie("RUE DU PAVILLON")
    compl_mock = MagicMock()
    compl_mock.execute.return_value = ([voie], [])
    fictif_mock = MagicMock()
    fictif_mock.execute.return_value = ([], [])  # ← manquait
    handle_compl_mock = MagicMock()
    handle_compl_mock.execute.return_value = "compl_result"
    # When
    res = use_case(compl_mock, fictif_mock, handle_compl=handle_compl_mock).execute([voie])
    # Then
    assert res == ["compl_result"]
    handle_compl_mock.execute.assert_called_once_with(voie)


def test_voie_fictive():
    # Given — pas de complément mais voie fictive détectée
    voie = _voie("LES VERNONS RUE B")
    compl_mock = MagicMock()
    compl_mock.execute.return_value = ([], [voie])
    fictif_mock = MagicMock()
    fictif_mock.execute.return_value = ([voie], [])
    assign_lib_compl_mock = MagicMock()
    assign_lib_compl_mock.execute.return_value = "lib_compl_result"
    # When
    res = use_case(compl_mock, fictif_mock, assign_lib_compl=assign_lib_compl_mock).execute([voie])
    # Then
    assert res == ["lib_compl_result"]
    assign_lib_compl_mock.execute.assert_called_once_with(voie)


def test_cas_general():
    # Given — ni complément ni voie fictive
    voie = _voie("CHE DES SEMAPHORES")
    compl_mock = MagicMock()
    compl_mock.execute.return_value = ([], [voie])
    fictif_mock = MagicMock()
    fictif_mock.execute.return_value = ([], [voie])
    not_compl_mock = MagicMock()
    not_compl_mock.execute.return_value = "general_result"
    # When
    res = use_case(compl_mock, fictif_mock, handle_not_compl_not_fictif=not_compl_mock).execute([voie])
    # Then
    assert res == ["general_result"]
    not_compl_mock.execute.assert_called_once_with(voie)
