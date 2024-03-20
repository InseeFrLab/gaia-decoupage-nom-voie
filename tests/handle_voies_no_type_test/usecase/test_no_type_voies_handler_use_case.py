from cProfile import label
from unittest.mock import MagicMock
from decoupage_libelles.handle_voies_no_type.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.finders.find_complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.handle_voies_no_type.usecase.handle_no_type_complement_use_case import HandleNoTypeComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase


def use_case(
    apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = MagicMock(),
    handle_no_type_complement_use_case: HandleNoTypeComplUseCase = MagicMock(),
    assign_lib_use_case: AssignLibUseCase = MagicMock(),
) -> NoTypeVoiesHandlerUseCase:
    return NoTypeVoiesHandlerUseCase(apply_complement_finder_on_voies_use_case, handle_no_type_complement_use_case, assign_lib_use_case)


def test_execute():
    # Given
    apply_complement_finder_on_voies_use_case = MagicMock()
    apply_complement_finder_on_voies_use_case.execute.return_value = (
        [
            InfoVoie(
                label_origin="",
                label_raw="",
                complement="",
            )
        ],
        [
            InfoVoie(
                label_origin="",
                label_raw="",
                complement="",
            ),
        ],
    )
    handle_no_type_complement_use_case = MagicMock()
    handle_no_type_complement_use_case.execute.return_value = VoieDecoupee(label_origin="")
    assign_lib_use_case = MagicMock()
    assign_lib_use_case.execute.return_value = VoieDecoupee(label_origin="")
    voies = []
    # When
    res = use_case(apply_complement_finder_on_voies_use_case, handle_no_type_complement_use_case, assign_lib_use_case).execute(voies)
    # Then
    assert len(res) == 2
