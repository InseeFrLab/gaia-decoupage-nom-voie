from unittest.mock import MagicMock
from decoupage_libelles.handle_voies_three_types_and_more.usecase.three_types_and_more_voies_handler_use_case import ThreeTypesAndMoreVoiesHandlerUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.handle_voies_one_type.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from decoupage_libelles.handle_voies_two_types.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase


def use_case(
    assign_lib_use_case: AssignLibUseCase = MagicMock(),
    assign_type_lib_use_case: AssignTypeLibUseCase = MagicMock(),
    generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = MagicMock(),
    generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = MagicMock(),
    one_type_voies_handler_use_case: OneTypeVoiesHandlerUseCase = MagicMock(),
    two_types_voies_handler_use_case: TwoTypesVoiesHandlerUseCase = MagicMock(),
) -> ThreeTypesAndMoreVoiesHandlerUseCase:
    return ThreeTypesAndMoreVoiesHandlerUseCase(
        assign_lib_use_case,
        assign_type_lib_use_case,
        generate_information_on_lib_use_case,
        generate_information_on_type_ordered_use_case,
        one_type_voies_handler_use_case,
        two_types_voies_handler_use_case,
    )


def test_e():
    # Given
    voies = [
        InfoVoie(
            label_origin="",
            label_raw="",
            complement="",
            types_and_positions={
                ("TYPE1", 1): (0, 5),
                ("TYPE2", 1): (10, 15),
                ("TYPE3", 1): (20, 25),
            },
        ),
        InfoVoie(label_origin="", label_raw="", complement=""),
        InfoVoie(label_origin="", label_raw="", complement=""),
    ]
    assign_lib_use_case = MagicMock()
    expeced_res = VoieDecoupee(label_origin="")
    assign_lib_use_case.execute.return_value = expeced_res
    assign_type_lib_use_case = MagicMock()
    generate_information_on_lib_use_case = MagicMock()
    generate_information_on_lib_use_case.execute.return_value = InfoVoie(has_type_in_first_pos=False, label_origin="", label_raw="", complement="")
    generate_information_on_type_ordered_use_case = MagicMock()
    one_type_voies_handler_use_case = MagicMock()
    two_types_voies_handler_use_case = MagicMock()
    # When
    res = use_case(
        assign_lib_use_case,
        assign_type_lib_use_case,
        generate_information_on_lib_use_case,
        generate_information_on_type_ordered_use_case,
        one_type_voies_handler_use_case,
        two_types_voies_handler_use_case,
    ).execute(voies)
    # Then
    generate_information_on_lib_use_case.execute.assert_called()
    print(res)
    assert res == [expeced_res]
