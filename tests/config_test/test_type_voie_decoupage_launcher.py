from unittest.mock import MagicMock
from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.clean_type_voie.usecase.type_voie_majic_preprocessor_use_case import TypeVoieMajicPreprocessorUseCase
from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from decoupage_libelles.handle_voies_no_type.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_two_types.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase
from decoupage_libelles.handle_voies_three_types_and_more.usecase.three_types_and_more_voies_handler_use_case import ThreeTypesAndMoreVoiesHandlerUseCase


def use_case(
    type_voie_majic_preprocessor_use_case: TypeVoieMajicPreprocessorUseCase = MagicMock(),
    voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = MagicMock(),
    no_type_voies_handler_use_case: NoTypeVoiesHandlerUseCase = MagicMock(),
    one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = MagicMock(),
    two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = MagicMock(),
    three_types_and_more_voies_handler_use_case: ThreeTypesAndMoreVoiesHandlerUseCase = MagicMock(),
):
    return TypeVoieDecoupageLauncher(
        type_voie_majic_preprocessor_use_case,
        voie_lib_preprocessor_use_case,
        no_type_voies_handler_use_case,
        one_type_voies_handler_use_case,
        two_types_voies_handler_use_case,
        three_types_and_more_voies_handler_use_case,
    )


def test_execute_voies_0():
    # Given
    voies_data = [""]
    voie_lib_preprocessor_use_case = MagicMock()
    voie_lib_preprocessor_use_case.execute.return_value = [InfoVoie(label_origin="", types_and_positions={})]
    no_type_voies_handler_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    no_type_voies_handler_use_case.execute.return_value = [expected_res]
    type_voie_majic_preprocessor_use_case = MagicMock()
    type_voie_majic_preprocessor_use_case.execute.return_value = (None, {})
    # When
    res = use_case(
        voie_lib_preprocessor_use_case=voie_lib_preprocessor_use_case,
        no_type_voies_handler_use_case=no_type_voies_handler_use_case,
        type_voie_majic_preprocessor_use_case=type_voie_majic_preprocessor_use_case,
    ).execute(voies_data)
    # Then
    no_type_voies_handler_use_case.execute.assert_called_once()
    assert res == [expected_res]


def test_execute_voies_1():
    # Given
    voies_data = [""]
    voie_lib_preprocessor_use_case = MagicMock()
    voie_lib_preprocessor_use_case.execute.return_value = [InfoVoie(label_origin="", types_and_positions={"RUE": (2, 3)})]
    one_type_voies_handler_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    one_type_voies_handler_use_case.execute.return_value = [expected_res]
    type_voie_majic_preprocessor_use_case = MagicMock()
    type_voie_majic_preprocessor_use_case.execute.return_value = (None, {})
    # When
    res = use_case(
        voie_lib_preprocessor_use_case=voie_lib_preprocessor_use_case,
        one_type_voies_handler_use_case=one_type_voies_handler_use_case,
        type_voie_majic_preprocessor_use_case=type_voie_majic_preprocessor_use_case,
    ).execute(voies_data)
    # Then
    one_type_voies_handler_use_case.execute.assert_called_once()
    assert res == [expected_res]


def test_execute_voies_2():
    # Given
    voies_data = [""]
    voie_lib_preprocessor_use_case = MagicMock()
    voie_lib_preprocessor_use_case.execute.return_value = [InfoVoie(label_origin="", types_and_positions={"RUE": (2, 3), "AV": (3, 5)})]
    two_types_voies_handler_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    two_types_voies_handler_use_case.execute.return_value = [expected_res]
    type_voie_majic_preprocessor_use_case = MagicMock()
    type_voie_majic_preprocessor_use_case.execute.return_value = (None, {})
    # When
    res = use_case(
        voie_lib_preprocessor_use_case=voie_lib_preprocessor_use_case,
        two_types_voies_handler_use_case=two_types_voies_handler_use_case,
        type_voie_majic_preprocessor_use_case=type_voie_majic_preprocessor_use_case,
    ).execute(voies_data)
    # Then
    two_types_voies_handler_use_case.execute.assert_called_once()
    assert res == [expected_res]


def test_execute_voies_3():
    # Given
    voies_data = [""]
    voie_lib_preprocessor_use_case = MagicMock()
    voie_lib_preprocessor_use_case.execute.return_value = [InfoVoie(label_origin="", types_and_positions={"RUE": (2, 3), "AV": (3, 5), "CH": (7, 9)})]
    three_types_and_more_voies_handler_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    three_types_and_more_voies_handler_use_case.execute.return_value = [expected_res]
    type_voie_majic_preprocessor_use_case = MagicMock()
    type_voie_majic_preprocessor_use_case.execute.return_value = (None, {})
    # When
    res = use_case(
        voie_lib_preprocessor_use_case=voie_lib_preprocessor_use_case,
        three_types_and_more_voies_handler_use_case=three_types_and_more_voies_handler_use_case,
        type_voie_majic_preprocessor_use_case=type_voie_majic_preprocessor_use_case,
    ).execute(voies_data)
    # Then
    three_types_and_more_voies_handler_use_case.execute.assert_called_once()
    assert res == [expected_res]
