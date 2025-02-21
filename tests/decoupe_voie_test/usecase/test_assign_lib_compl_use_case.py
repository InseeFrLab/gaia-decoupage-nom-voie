from unittest.mock import MagicMock
from decoupage_libelles.decoupe_voie.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


def use_case(
    get_words_between_use_case: GetWordsBetweenUseCase = MagicMock(),
    order_type_in_lib_use_case: OrderTypeInLib = MagicMock(),
):
    return AssignLibComplUseCase(get_words_between_use_case, order_type_in_lib_use_case)


def test_assign_lib_compl_use_case():
    # Given
    infovoie = InfoVoie()
    get_words_between_use_case = MagicMock()
    order_type_in_lib_use_case = MagicMock()
    order_type_in_lib_use_case.execute.return_value = InformationOnTypeOrdered(
        type_name="",
        order_in_lib=1,
        position_start=1,
        position_end=1,
        occurence=1,
    )
    get_words_between_use_case.execute.side_effect = ["label_assigned", "compl_assigned"]
    # When
    res = use_case(get_words_between_use_case, order_type_in_lib_use_case).execute(infovoie)
    # Then
    assert res == VoieDecoupee(
        label_origin=infovoie.label_origin,
        type_assigned=" ",
        label_assigned="label_assigned",
        compl_assigned="compl_assigned",
        compl2=infovoie.complement,
    )
