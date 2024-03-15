from unittest.mock import MagicMock
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase


def use_case(get_words_between_use_case: GetWordsBetweenUseCase):
    return AssignComplTypeLibUseCase(get_words_between_use_case)


def test_assign_compl_type_lib_use_case():
    # Given
    infovoie = InfoVoie(
        label_origin="",
        complement="",
        label_raw="",
    )
    type_principal = InformationOnTypeOrdered(
        type_name="",
        position_start=1,
        position_end=3,
        occurence=1,
        order_in_lib=1,
    )
    get_words_between_use_case = MagicMock()
    get_words_between_use_case.execute.side_effect = ["label_assigned", "compl_assigned"]
    # When
    res = use_case(get_words_between_use_case).execute(infovoie, type_principal)
    # Then
    assert res == VoieDecoupee(
        label_origin=infovoie.label_origin,
        type_assigned=type_principal.type_name,
        label_assigned="label_assigned",
        compl_assigned="compl_assigned",
        compl2=infovoie.complement,
    )
