from unittest.mock import MagicMock
from decoupage_libelles.finders.find_type.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase
from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.remove_type_from_lib_and_types_use_case import RemoveTypeFromLibAndTypesUseCase
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


def use_case(remove_type_from_lib_and_types_use_case: RemoveTypeFromLibAndTypesUseCase = MagicMock()) -> RemoveDuplicatesUseCase:
    return RemoveDuplicatesUseCase(remove_type_from_lib_and_types_use_case)


def test_duplications():
    # Given
    info_voie = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
        types_and_positions={
            ("ART", 1): (0, 4),
            ("ART", 2): (5, 8),
            ("RUE", 1): (10, 13),
            ("RUE", 2): (14, 17),
            ("ROUTE", 1): (20, 25),
            ("ROUTE", 2): (26, 31),
            ("ROUTE", 3): (32, 37),
            ("ROUTE", 4): (38, 43),
        },
    )
    type_finder_object = TypeFinderObject(
        voie_big=info_voie,
        type_data=TypeFinderUtils(
            type_voie_df=None,
            code2lib={},
        ),
    )
    remove_type_from_lib_and_types_use_case = MagicMock()
    mock_res = MagicMock()
    remove_type_from_lib_and_types_use_case.execute.return_value = mock_res
    # When
    use_case(remove_type_from_lib_and_types_use_case).execute(type_finder_object)
    # Then
    assert remove_type_from_lib_and_types_use_case.execute.call_count == 1


def test_execute_retourne_type_finder_object_vide_si_pas_de_duplications():
    info_voie = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
        types_and_positions={
            ("ART", 1): (0, 4),
            ("RUE", 1): (10, 13),
            ("ROUTE", 1): (20, 25),
        },
    )
    type_finder_object = TypeFinderObject(
        voie_big=info_voie,
        type_data=TypeFinderUtils(
            type_voie_df=None,
            code2lib={},
        ),
    )
    # When
    res = use_case().execute(type_finder_object)
    # Then
    assert len(res.voie_big.types_and_positions) == 3
