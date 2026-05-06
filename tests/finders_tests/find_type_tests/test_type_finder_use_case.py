from unittest.mock import MagicMock

from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.finders.find_type.usecase.detect_types_use_case import DetectTypesUseCase
from decoupage_libelles.finders.find_type.usecase.update_occurrences_by_order_use_case import UpdateOccurrencesByOrderUseCase
from decoupage_libelles.finders.find_type.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase
from decoupage_libelles.finders.find_type.usecase.remove_wrong_detections_use_case import RemoveWrongDetectionsUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_type.usecase.type_finder_use_case import TypeFinderUseCase


def use_case(
    detect_types_use_case: DetectTypesUseCase = MagicMock(),
    update_occurrences_by_order_use_case: UpdateOccurrencesByOrderUseCase = MagicMock(),
    remove_duplicates_use_case: RemoveDuplicatesUseCase = MagicMock(),
    remove_wrong_detections_use_case: RemoveWrongDetectionsUseCase = MagicMock(),
) -> TypeFinderUseCase:
    return TypeFinderUseCase(
        detect_types_use_case,
        update_occurrences_by_order_use_case,
        remove_duplicates_use_case,
        remove_wrong_detections_use_case,
    )


def _make_type_finder_object(label_preproc: list, types_and_positions: dict = None) -> TypeFinderObject:
    voie_big = InfoVoie()
    voie_big.label_preproc = label_preproc
    voie_big.types_and_positions = types_and_positions or {}
    return TypeFinderObject(voie_big=voie_big, type_data=TypeFinderUtils())


def test_voie_sep_et_voie_initialises_avant_detection():
    # Given
    detect_mock = MagicMock()
    detect_mock.execute.side_effect = lambda obj: obj
    obj = _make_type_finder_object(["AV", "VICTOR", "HUGO"])
    # When
    use_case(detect_types_use_case=detect_mock).execute(obj)
    # Then — voie_sep et voie doivent être initialisés avant l'appel à detect
    called_obj = detect_mock.execute.call_args[0][0]
    assert called_obj.voie_sep == ["AV", "VICTOR", "HUGO"]
    assert called_obj.voie == "AV VICTOR HUGO"


def test_detect_types_toujours_appele():
    # Given
    detect_mock = MagicMock()
    detect_mock.execute.side_effect = lambda obj: obj
    obj = _make_type_finder_object(["AV", "VICTOR"])
    # When
    use_case(detect_types_use_case=detect_mock).execute(obj)
    # Then
    detect_mock.execute.assert_called_once()


def test_nettoyage_non_appele_si_un_seul_type():
    # Given — detect ne trouve qu'un seul type
    voie_big = InfoVoie()
    voie_big.label_preproc = ["AV", "VICTOR"]
    voie_big.types_and_positions = {("AVENUE", 1): (0, 0)}

    detect_mock = MagicMock()
    detect_mock.execute.side_effect = lambda obj: obj

    update_mock = MagicMock()
    remove_dup_mock = MagicMock()
    remove_wrong_mock = MagicMock()

    obj = TypeFinderObject(voie_big=voie_big, type_data=TypeFinderUtils())
    # When
    use_case(detect_mock, update_mock, remove_dup_mock, remove_wrong_mock).execute(obj)
    # Then — les étapes de nettoyage ne doivent pas être appelées
    update_mock.execute.assert_not_called()
    remove_dup_mock.execute.assert_not_called()
    remove_wrong_mock.execute.assert_not_called()


def test_nettoyage_appele_si_plusieurs_types():
    # Given — detect trouve deux types
    voie_big = InfoVoie()
    voie_big.label_preproc = ["AV", "RUE"]
    voie_big.types_and_positions = {("AVENUE", 1): (0, 0), ("RUE", 1): (1, 1)}

    detect_mock = MagicMock()
    detect_mock.execute.side_effect = lambda obj: obj
    update_mock = MagicMock()
    update_mock.execute.side_effect = lambda obj: obj
    remove_dup_mock = MagicMock()
    remove_dup_mock.execute.side_effect = lambda obj: obj
    remove_wrong_mock = MagicMock()
    remove_wrong_mock.execute.side_effect = lambda obj: obj

    obj = TypeFinderObject(voie_big=voie_big, type_data=TypeFinderUtils())
    # When
    use_case(detect_mock, update_mock, remove_dup_mock, remove_wrong_mock).execute(obj)
    # Then — les trois étapes de nettoyage doivent être appelées dans l'ordre
    update_mock.execute.assert_called_once()
    remove_dup_mock.execute.assert_called_once()
    remove_wrong_mock.execute.assert_called_once()


def test_retourne_infovoie():
    # Given
    detect_mock = MagicMock()
    detect_mock.execute.side_effect = lambda obj: obj
    obj = _make_type_finder_object(["AV", "VICTOR"])
    # When
    res = use_case(detect_types_use_case=detect_mock).execute(obj)
    # Then — doit retourner le voie_big (InfoVoie), pas le TypeFinderObject
    assert isinstance(res, InfoVoie)
