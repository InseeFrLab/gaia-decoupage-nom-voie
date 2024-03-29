from unittest.mock import MagicMock
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


def use_case(
    get_words_between_use_case: GetWordsBetweenUseCase = MagicMock(),
    order_type_in_lib_use_case: OrderTypeInLib = MagicMock(),
):
    return AssignTypeLibComplUseCase(get_words_between_use_case, order_type_in_lib_use_case)


def test_assign_type_lib_compl_use_case_types_non_definis():
    # Given
    infovoie = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
    )
    get_words_between_use_case = MagicMock()
    get_words_between_use_case.execute.side_effect = ["label_assigned", "compl_assigned"]
    order_type_in_lib_use_case = MagicMock()
    order_type_in_lib_use_case.execute.side_effect = [
        InformationOnTypeOrdered(
            type_name="type_name",
            order_in_lib=1,
            position_start=1,
            position_end=1,
            occurence=1,
        ),
        InformationOnTypeOrdered(
            type_name="",
            order_in_lib=2,
            position_start=2,
            position_end=2,
            occurence=2,
        ),
    ]
    # When
    res = use_case(get_words_between_use_case, order_type_in_lib_use_case).execute(infovoie)
    # Then
    assert res == VoieDecoupee(
        label_origin=infovoie.label_origin,
        type_assigned="type_name",
        label_assigned="label_assigned",
        compl_assigned="compl_assigned",
        compl2=infovoie.complement,
    )


def test_assign_type_lib_compl_use_case_types_definis():
    # Given
    infovoie = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
    )
    type_principal = InformationOnTypeOrdered(
        type_name="type_name",
        order_in_lib=1,
        position_start=1,
        position_end=1,
        occurence=1,
    )
    type_compl = InformationOnTypeOrdered(
        type_name="",
        order_in_lib=2,
        position_start=2,
        position_end=2,
        occurence=2,
    )
    get_words_between_use_case = MagicMock()
    get_words_between_use_case.execute.side_effect = ["label_assigned", "compl_assigned"]
    # When
    res = use_case(get_words_between_use_case).execute(infovoie, type_principal, type_compl)
    # Then
    assert res == VoieDecoupee(
        label_origin=infovoie.label_origin,
        type_assigned="type_name",
        label_assigned="label_assigned",
        compl_assigned="compl_assigned",
        compl2=infovoie.complement,
    )
