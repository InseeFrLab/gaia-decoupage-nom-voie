from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.detect_codified_types_use_case import DetectCodifiedTypesUseCase
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


def use_case():
    return DetectCodifiedTypesUseCase()


def test_execute_with_empty_type_data():
    # Given
    type_finder_object: TypeFinderObject = TypeFinderObject(
        voie_big=InfoVoie(
            label_raw="",
            label_origin="",
            complement="",
            types_and_positions={},
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            codes=[],
            code2lib=None,
        ),
    )
    # When
    res = use_case().execute(type_finder_object)
    # Then
    assert res == type_finder_object
    assert len(res.voie_big.types_and_positions) == 0


def test_execute_():
    # Given
    type_finder_object: TypeFinderObject = TypeFinderObject(
        voie_big=InfoVoie(
            label_raw="",
            label_origin="",
            complement="",
            types_and_positions={},
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            codes=["C1", "C2"],
            code2lib={"C1": "lib1", "C2": "lib2"},
        ),
        voie_sep=["C1", "C2", "C1"],
    )
    # When
    res = use_case().execute(type_finder_object)
    # Then
    assert res == type_finder_object
    assert len(res.voie_big.types_and_positions) == 3
    assert {("lib1", 1): (0, 0), ("lib1", 2): (2, 2), ("lib2", 1): (1, 1)} == res.voie_big.types_and_positions
