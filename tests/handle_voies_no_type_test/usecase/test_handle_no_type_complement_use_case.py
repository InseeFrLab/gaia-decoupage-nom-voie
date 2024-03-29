from unittest.mock import MagicMock
from decoupage_libelles.handle_voies_no_type.usecase.handle_no_type_complement_use_case import HandleNoTypeComplUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


def use_case(
    generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = MagicMock(),
    generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = MagicMock(),
    assign_lib_compl_use_case: AssignLibComplUseCase = MagicMock(),
    assign_lib_use_case: AssignLibUseCase = MagicMock(),
) -> HandleNoTypeComplUseCase:
    return HandleNoTypeComplUseCase(generate_information_on_lib_use_case, generate_information_on_type_ordered_use_case, assign_lib_compl_use_case, assign_lib_use_case)


def test_is_in_middle_position_and_not_has_adj_det_before():
    # Given
    voie_compl = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
    )
    generate_information_on_lib_use_case = MagicMock()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.return_value = InformationOnTypeOrdered(
        type_name="type",
        order_in_lib=1,
        position_start=1,
        position_end=3,
        occurence=1,
        is_in_middle_position=True,
        has_adj_det_before=False,
    )
    assign_lib_compl_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    assign_lib_compl_use_case.execute.return_value = expected_res
    # When
    res: VoieDecoupee = use_case(generate_information_on_lib_use_case, generate_information_on_type_ordered_use_case, assign_lib_compl_use_case, MagicMock()).execute(voie_compl)
    # Then
    assert expected_res == res


def test_is_in_middle_position_and_has_adj_det_before():
    # Given
    voie_compl = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
    )
    generate_information_on_lib_use_case = MagicMock()
    generate_information_on_type_ordered_use_case = MagicMock()
    generate_information_on_type_ordered_use_case.execute.return_value = InformationOnTypeOrdered(
        type_name="type",
        order_in_lib=1,
        position_start=1,
        position_end=3,
        occurence=1,
        is_in_middle_position=True,
        has_adj_det_before=True,
    )
    assign_lib_use_case = MagicMock()
    expected_res = VoieDecoupee(label_origin="")
    assign_lib_use_case.execute.return_value = expected_res
    # When
    res: VoieDecoupee = use_case(generate_information_on_lib_use_case, generate_information_on_type_ordered_use_case, MagicMock(), assign_lib_use_case).execute(voie_compl)
    # Then
    assert expected_res == res
