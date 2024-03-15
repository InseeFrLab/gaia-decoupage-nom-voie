from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee


def use_case():
    return AssignLibUseCase()


def test_assign_lib_use_case():
    # Given
    infovoie = InfoVoie(
        label_origin="",
        label_raw="",
        complement="",
        label_preproc=["A", "B", "C"],
    )
    # When
    res = use_case().execute(infovoie)
    # Then
    assert res == VoieDecoupee(
        label_origin=infovoie.label_origin,
        type_assigned=" ",
        label_assigned="A B C",
        compl_assigned=" ",
        compl2=infovoie.complement,
    )
