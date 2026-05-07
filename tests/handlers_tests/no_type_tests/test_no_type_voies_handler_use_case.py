from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.handlers.no_type.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from decoupage_libelles.finders.complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.handlers.no_type.usecase.handle_no_type_complement_use_case import HandleNoTypeComplUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_use_case import AssignLibUseCase


def use_case(
    apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = MagicMock(),
    handle_no_type_complement_use_case: HandleNoTypeComplUseCase = MagicMock(),
    assign_lib_use_case: AssignLibUseCase = MagicMock(),
) -> NoTypeVoiesHandlerUseCase:
    return NoTypeVoiesHandlerUseCase(
        apply_complement_finder_on_voies_use_case,
        handle_no_type_complement_use_case,
        assign_lib_use_case,
    )


def _voie(label: str) -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = label.upper().split()
    v.types_and_positions = {}
    return v


def test_voies_sans_complement_assignees_en_lib():
    # Given — aucun complément trouvé
    voie = _voie("LES HARDONNIERES")
    complement_mock = MagicMock()
    complement_mock.execute.return_value = ([], [voie])
    assign_lib_mock = MagicMock()
    assign_lib_mock.execute.return_value = "lib_result"
    # When
    res = use_case(complement_mock, MagicMock(), assign_lib_mock).execute([voie])
    # Then
    assert res == ["lib_result"]
    assign_lib_mock.execute.assert_called_once_with(voie)


def test_voies_avec_complement_passees_au_handler_complement():
    # Given — un complément trouvé
    voie = _voie("LE TILLET BAT A")
    complement_mock = MagicMock()
    complement_mock.execute.return_value = ([voie], [])
    handle_compl_mock = MagicMock()
    handle_compl_mock.execute.return_value = "compl_result"
    # When
    res = use_case(complement_mock, handle_compl_mock, MagicMock()).execute([voie])
    # Then
    assert res == ["compl_result"]
    handle_compl_mock.execute.assert_called_once_with(voie)


def test_liste_vide():
    # Given
    complement_mock = MagicMock()
    complement_mock.execute.return_value = ([], [])
    # When
    res = use_case(complement_mock).execute([])
    # Then
    assert res == []


def test_ordre_complement_avant_lib():
    # Given — une voie avec complément, une sans
    voie_compl = _voie("BAT JEAN LAMOUR")
    voie_lib   = _voie("LES HARDONNIERES")
    complement_mock = MagicMock()
    complement_mock.execute.return_value = ([voie_compl], [voie_lib])
    handle_compl_mock = MagicMock()
    handle_compl_mock.execute.return_value = "compl_result"
    assign_lib_mock = MagicMock()
    assign_lib_mock.execute.return_value = "lib_result"
    # When
    res = use_case(complement_mock, handle_compl_mock, assign_lib_mock).execute([voie_compl, voie_lib])
    # Then — complément traité en premier dans la liste résultat
    assert res == ["compl_result", "lib_result"]
