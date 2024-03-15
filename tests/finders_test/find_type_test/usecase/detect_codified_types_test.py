from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.detect_codified_types_use_case import DetectCodifiedTypesUseCase
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import TypeFinderUtils


def use_case():
    return DetectCodifiedTypesUseCase()


def test_execute_with_empty_type_data():
    # Given
    type_finder_object: TypeFinderObject = TypeFinderObject(
        voie_big=None,
        type_data=TypeFinderUtils(
            type_voie_df=None,
            codes=[],
            code2lib=None,
        ),
    )
    # When
    res = use_case().execute(type_finder_object)
    print(res)
    # Then
    assert res == type_finder_object
