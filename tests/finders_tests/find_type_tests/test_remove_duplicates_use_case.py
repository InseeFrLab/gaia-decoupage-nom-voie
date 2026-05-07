from unittest.mock import MagicMock

from decoupage_libelles.finders.type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.finders.type.usecase.remove_type_from_lib_use_case import RemoveTypeFromLibUseCase
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.finders.type.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase


def use_case(
    remove_type_from_lib_use_case: RemoveTypeFromLibUseCase = MagicMock(),
) -> RemoveDuplicatesUseCase:
    return RemoveDuplicatesUseCase(remove_type_from_lib_use_case)


def _make_type_finder_object(label_preproc: list, types_and_positions: dict) -> TypeFinderObject:
    voie_big = InfoVoie()
    voie_big.label_preproc = label_preproc
    voie_big.types_and_positions = types_and_positions
    return TypeFinderObject(voie_big=voie_big, type_data=TypeFinderUtils())


def test_sans_doublon_rien_ne_change():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR"],
        types_and_positions={("AVENUE", 1): (0, 0)},
    )
    # When
    res = use_case().execute(obj)
    # Then
    assert ("AVENUE", 1) in res.voie_big.types_and_positions


def test_deux_types_differents_conserves():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "RUE"],
        types_and_positions={("AVENUE", 1): (0, 0), ("RUE", 1): (2, 2)},
    )
    # When
    res = use_case().execute(obj)
    # Then
    assert len(res.voie_big.types_and_positions) == 2


def test_doublon_non_adjacent_conserve():
    # Given — deux AVENUE séparées par 2 positions (non adjacentes, distance > 1)
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "AV", "HUGO"],
        types_and_positions={("AVENUE", 1): (0, 0), ("AVENUE", 2): (2, 2)},
    )
    # When
    res = use_case().execute(obj)
    # Then — aucune suppression car pas adjacentes (pos2[0] - pos1[1] = 2 ≠ 1)
    assert ("AVENUE", 1) in res.voie_big.types_and_positions
    assert ("AVENUE", 2) in res.voie_big.types_and_positions


def test_doublon_adjacent_appelle_remove_type_from_lib():
    # Given — "ABE ABBAYE" : ABE et ABBAYE sont deux variantes adjacentes du même canonique ABBAYE
    remove_mock = MagicMock()
    remove_mock.execute.side_effect = lambda infovoie, s, e: infovoie
    obj = _make_type_finder_object(
        label_preproc=["ABE", "ABBAYE"],
        types_and_positions={("ABBAYE", 1): (0, 0), ("ABBAYE", 2): (1, 1)},
    )
    # When
    use_case(remove_mock).execute(obj)
    # Then — remove_type_from_lib doit avoir été appelé pour retirer le plus court (ABE)
    remove_mock.execute.assert_called_once()


def test_doublon_adjacent_retire_occurrence_courte():
    # Given — "ABE ABBAYE" : ABE en (0,0) et ABBAYE en (1,1) adjacents
    remove_mock = MagicMock()
    remove_mock.execute.side_effect = lambda infovoie, s, e: infovoie
    obj = _make_type_finder_object(
        label_preproc=["ABE", "ABBAYE"],
        types_and_positions={("ABBAYE", 1): (0, 0), ("ABBAYE", 2): (1, 1)},
    )
    # When
    res = use_case(remove_mock).execute(obj)
    # Then
    assert ("ABBAYE", 2) not in res.voie_big.types_and_positions
