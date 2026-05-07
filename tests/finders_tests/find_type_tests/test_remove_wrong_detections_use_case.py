from unittest.mock import MagicMock

from decoupage_libelles.finders.type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.finders.type.usecase.remove_type_from_lib_use_case import RemoveTypeFromLibUseCase
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.finders.type.usecase.remove_wrong_detections_use_case import RemoveWrongDetectionsUseCase


def use_case(
    remove_type_from_lib_use_case: RemoveTypeFromLibUseCase = MagicMock(),
    generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = MagicMock(),
) -> RemoveWrongDetectionsUseCase:
    return RemoveWrongDetectionsUseCase(remove_type_from_lib_use_case, generate_information_on_type_ordered_use_case)


def _make_type_finder_object(label_preproc: list, types_and_positions: dict) -> TypeFinderObject:
    voie_big = InfoVoie()
    voie_big.label_preproc = label_preproc
    voie_big.types_and_positions = types_and_positions
    return TypeFinderObject(voie_big=voie_big, type_data=TypeFinderUtils())


def _make_type_info(type_name: str, position_start: int, position_end: int, occurence: int):
    info = MagicMock()
    info.type_name = type_name
    info.position_start = position_start
    info.position_end = position_end
    info.occurence = occurence
    return info


def test_un_seul_type_rien_ne_change():
    # Given — un seul type détecté, la boucle while ne s'exécute pas
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR"],
        types_and_positions={("AVENUE", 1): (0, 0)},
    )
    # When
    res = use_case().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {("AVENUE", 1): (0, 0)}


def test_deux_types_sans_lien_conserves():
    # Given — AVENUE et RUE n'ont aucun lien : aucune suppression
    get_info = MagicMock()
    get_info.execute.side_effect = [
        _make_type_info("AVENUE", 0, 0, 1),
        _make_type_info("RUE", 2, 2, 1),
    ]
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "RUE"],
        types_and_positions={("AVENUE", 1): (0, 0), ("RUE", 1): (2, 2)},
    )
    # When
    res = use_case(generate_information_on_type_ordered_use_case=get_info).execute(obj)
    # Then
    assert ("AVENUE", 1) in res.voie_big.types_and_positions
    assert ("RUE", 1) in res.voie_big.types_and_positions


def test_type_court_inclus_dans_long_supprime_sans_retrait_libelle():
    # Given — CHEMIN inclus dans le span de ANCIEN CHEMIN (s_long=0 <= s_court=1 <= e_long=1)
    get_info = MagicMock()
    get_info.execute.side_effect = [
        _make_type_info("CHEMIN", 1, 1, 1),
        _make_type_info("ANCIEN CHEMIN", 0, 1, 1),
    ]
    remove_mock = MagicMock()
    obj = _make_type_finder_object(
        label_preproc=["ANC", "CHEM", "DES", "PINS"],
        types_and_positions={("CHEMIN", 1): (1, 1), ("ANCIEN CHEMIN", 1): (0, 1)},
    )
    # When
    res = use_case(remove_mock, get_info).execute(obj)
    # Then — CHEMIN supprimé, remove_type_from_lib NON appelé (pas de retrait libellé)
    assert ("CHEMIN", 1) not in res.voie_big.types_and_positions
    assert ("ANCIEN CHEMIN", 1) in res.voie_big.types_and_positions
    remove_mock.execute.assert_not_called()


def test_type_court_adjacent_supprime_avec_retrait_libelle():
    # Given — ROUTE adjacent à ANCIENNE ROUTE (s_long - e_court == 1)
    get_info = MagicMock()
    get_info.execute.side_effect = [
        _make_type_info("ROUTE", 0, 0, 1),
        _make_type_info("ANCIENNE ROUTE", 1, 2, 1),
    ]
    remove_mock = MagicMock()
    remove_mock.execute.side_effect = lambda infovoie, s, e: infovoie
    obj = _make_type_finder_object(
        label_preproc=["ROUTE", "ANCIENNE", "ROUTE"],
        types_and_positions={("ROUTE", 1): (0, 0), ("ANCIENNE ROUTE", 1): (1, 2)},
    )
    # When
    res = use_case(remove_mock, get_info).execute(obj)
    # Then — ROUTE supprimé ET remove_type_from_lib appelé
    assert ("ROUTE", 1) not in res.voie_big.types_and_positions
    remove_mock.execute.assert_called_once()


def test_types_identiques_ignores():
    # Given — les deux types ont le même nom : on passe sans rien faire
    get_info = MagicMock()
    get_info.execute.side_effect = [
        _make_type_info("AVENUE", 0, 0, 1),
        _make_type_info("AVENUE", 2, 2, 2),
    ]
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "AV"],
        types_and_positions={("AVENUE", 1): (0, 0), ("AVENUE", 2): (2, 2)},
    )
    # When
    res = use_case(generate_information_on_type_ordered_use_case=get_info).execute(obj)
    # Then — aucune suppression
    assert len(res.voie_big.types_and_positions) == 2
