from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.finders.type.usecase.remove_type_from_lib_use_case import RemoveTypeFromLibUseCase


def _make_infovoie(label_preproc: list, types_and_positions: dict) -> InfoVoie:
    voie = InfoVoie()
    voie.label_preproc = label_preproc
    voie.types_and_positions = types_and_positions
    return voie


def test_retire_mot_unique_en_debut():
    # Given
    infovoie = _make_infovoie(
        label_preproc=["AV", "VICTOR", "HUGO"],
        types_and_positions={("AVENUE", 1): (0, 0)},
    )
    # When
    res = RemoveTypeFromLibUseCase().execute(infovoie, pos_start=0, pos_end=0)
    # Then
    assert res.label_preproc == ["VICTOR", "HUGO"]


def test_retire_mot_unique_au_milieu():
    # Given
    infovoie = _make_infovoie(
        label_preproc=["VICTOR", "AV", "HUGO"],
        types_and_positions={("AVENUE", 1): (1, 1)},
    )
    # When
    res = RemoveTypeFromLibUseCase().execute(infovoie, pos_start=1, pos_end=1)
    # Then
    assert res.label_preproc == ["VICTOR", "HUGO"]


def test_retire_groupe_multi_mots():
    # Given
    infovoie = _make_infovoie(
        label_preproc=["ANC", "CHEM", "DES", "PINS"],
        types_and_positions={("ANCIEN CHEMIN", 1): (0, 1)},
    )
    # When
    res = RemoveTypeFromLibUseCase().execute(infovoie, pos_start=0, pos_end=1)
    # Then
    assert res.label_preproc == ["DES", "PINS"]


def test_decale_positions_apres_suppression():
    # Given — ROUTE en (0,0), AVENUE en (3,3) : après suppression de ROUTE, AVENUE passe en (2,2)
    infovoie = _make_infovoie(
        label_preproc=["RTE", "VICTOR", "HUGO", "AV"],
        types_and_positions={("ROUTE", 1): (0, 0), ("AVENUE", 1): (3, 3)},
    )
    # When
    res = RemoveTypeFromLibUseCase().execute(infovoie, pos_start=0, pos_end=0)
    # Then
    assert res.types_and_positions[("AVENUE", 1)] == (2, 2)


def test_ne_decale_pas_positions_avant_suppression():
    # Given — suppression en fin : AVENUE en (0,0) ne doit pas être décalée
    infovoie = _make_infovoie(
        label_preproc=["AV", "VICTOR", "RTE"],
        types_and_positions={("AVENUE", 1): (0, 0), ("ROUTE", 1): (2, 2)},
    )
    # When
    res = RemoveTypeFromLibUseCase().execute(infovoie, pos_start=2, pos_end=2)
    # Then
    assert res.types_and_positions[("AVENUE", 1)] == (0, 0)


def test_decale_positions_apres_suppression_groupe():
    # Given — suppression de 2 mots : AVENUE en (4,4) passe en (2,2)
    infovoie = _make_infovoie(
        label_preproc=["ANC", "CHEM", "DES", "PINS", "AV"],
        types_and_positions={("ANCIEN CHEMIN", 1): (0, 1), ("AVENUE", 1): (4, 4)},
    )
    # When
    res = RemoveTypeFromLibUseCase().execute(infovoie, pos_start=0, pos_end=1)
    # Then
    assert res.types_and_positions[("AVENUE", 1)] == (2, 2)
