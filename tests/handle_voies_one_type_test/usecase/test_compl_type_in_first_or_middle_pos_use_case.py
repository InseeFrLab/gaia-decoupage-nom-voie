from unittest.mock import MagicMock
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_middle_pos_use_case import ComplTypeInFirstOrMiddlePosUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


def use_case(
    generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = MagicMock(),
    generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = MagicMock(),
    assign_type_lib_use_case: AssignTypeLibUseCase = MagicMock(),
    assign_lib_use_case: AssignLibUseCase = MagicMock(),
    assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = MagicMock(),
    assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = MagicMock(),
):
    return ComplTypeInFirstOrMiddlePosUseCase(
        generate_information_on_lib_use_case,
        generate_information_on_type_ordered_use_case,
        assign_type_lib_use_case,
        assign_lib_use_case,
        assign_compl_type_lib_use_case,
        assign_type_lib_compl_use_case,
    )


def test_execute_no_complement():
    # Given
    voie_compl = InfoVoie()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.side_effect = [
        InformationOnTypeOrdered(is_complement=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
        InformationOnTypeOrdered(is_complement=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
    ]
    # When
    res = use_case(generate_information_on_type_ordered_use_case=generate_information_on_type_ordered_use_case).execute(voie_compl)
    # Then
    assert res is None


def test_execute_complement_1():
    # Given
    voie_compl = InfoVoie()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.side_effect = [
        InformationOnTypeOrdered(is_complement=True, has_adj_det_before=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
        InformationOnTypeOrdered(is_complement=False, has_adj_det_before=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
    ]
    assign_compl_type_lib_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    assign_compl_type_lib_use_case.execute.return_value = expected_res
    # When
    res = use_case(
        generate_information_on_type_ordered_use_case=generate_information_on_type_ordered_use_case,
        assign_compl_type_lib_use_case=assign_compl_type_lib_use_case,
    ).execute(voie_compl)
    # Then
    assert res == expected_res


def test_execute_complement_1_has_adj_det_before():
    # Given
    voie_compl = InfoVoie()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.side_effect = [
        InformationOnTypeOrdered(is_complement=True, has_adj_det_before=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
        InformationOnTypeOrdered(is_complement=False, has_adj_det_before=True, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
    ]
    assign_lib_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    assign_lib_use_case.execute.return_value = expected_res
    # When
    res = use_case(
        generate_information_on_type_ordered_use_case=generate_information_on_type_ordered_use_case,
        assign_lib_use_case=assign_lib_use_case,
    ).execute(voie_compl)
    # Then
    assert res == expected_res


def test_execute_complement_2():
    # Given
    voie_compl = InfoVoie()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.side_effect = [
        InformationOnTypeOrdered(is_complement=False, has_adj_det_before=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
        InformationOnTypeOrdered(is_complement=True, has_adj_det_before=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
    ]
    assign_type_lib_compl_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    assign_type_lib_compl_use_case.execute.return_value = expected_res
    # When
    res = use_case(
        generate_information_on_type_ordered_use_case=generate_information_on_type_ordered_use_case,
        assign_type_lib_compl_use_case=assign_type_lib_compl_use_case,
    ).execute(voie_compl)
    # Then
    assert res == expected_res


def test_execute_complement_2_has_adj_det_before():
    # Given
    voie_compl = InfoVoie()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.side_effect = [
        InformationOnTypeOrdered(is_complement=False, has_adj_det_before=False, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
        InformationOnTypeOrdered(is_complement=True, has_adj_det_before=True, type_name="", order_in_lib=1, position_start=1, position_end=1, occurence=1),
    ]
    assign_type_lib_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    assign_type_lib_use_case.execute.return_value = expected_res
    # When
    res = use_case(
        generate_information_on_type_ordered_use_case=generate_information_on_type_ordered_use_case,
        assign_type_lib_use_case=assign_type_lib_use_case,
    ).execute(voie_compl)
    # Then
    assert res == expected_res
