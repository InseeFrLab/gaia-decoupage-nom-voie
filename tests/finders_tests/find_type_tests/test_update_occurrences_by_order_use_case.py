from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_type.usecase.update_occurrences_by_order_use_case import UpdateOccurrencesByOrderUseCase


def _make_type_finder_object(types_and_positions: dict) -> TypeFinderObject:
    voie_big = InfoVoie()
    voie_big.types_and_positions = types_and_positions
    return TypeFinderObject(voie_big=voie_big, type_data=TypeFinderUtils())


def test_types_tries_par_position_croissante():
    # Given — AVENUE en position 3, RUE en position 0
    obj = _make_type_finder_object({
        ("AVENUE", 1): (3, 3),
        ("RUE", 1): (0, 0),
    })
    # When
    res = UpdateOccurrencesByOrderUseCase().execute(obj)
    # Then
    keys = list(res.voie_big.types_and_positions.keys())
    assert keys[0][0] == "RUE"
    assert keys[1][0] == "AVENUE"


def test_occurrences_renumerotees_par_ordre_apparition():
    # Given — AVENUE mal numérotée : celle en pos 0 porte l'occurrence 2
    obj = _make_type_finder_object({
        ("AVENUE", 2): (0, 0),
        ("AVENUE", 1): (4, 4),
    })
    # When
    res = UpdateOccurrencesByOrderUseCase().execute(obj)
    # Then — après tri, la pos 0 doit porter l'occurrence 1
    assert res.voie_big.types_and_positions[("AVENUE", 1)] == (0, 0)
    assert res.voie_big.types_and_positions[("AVENUE", 2)] == (4, 4)


def test_types_differents_compteurs_independants():
    # Given
    obj = _make_type_finder_object({
        ("RUE", 1): (2, 2),
        ("AVENUE", 1): (0, 0),
    })
    # When
    res = UpdateOccurrencesByOrderUseCase().execute(obj)
    # Then — chaque type garde son occurrence 1
    assert ("RUE", 1) in res.voie_big.types_and_positions
    assert ("AVENUE", 1) in res.voie_big.types_and_positions


def test_un_seul_type_inchange():
    # Given
    obj = _make_type_finder_object({("CHEMIN", 1): (0, 0)})
    # When
    res = UpdateOccurrencesByOrderUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {("CHEMIN", 1): (0, 0)}
