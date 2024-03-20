from decoupage_libelles.finders.find_type.usecase.remove_type_from_lib_and_types_use_case import RemoveTypeFromLibAndTypesUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


def use_case() -> RemoveTypeFromLibAndTypesUseCase:
    return RemoveTypeFromLibAndTypesUseCase()


def test_execute_supprime_type_et_recale_positions():
    # Given
    infovoie = InfoVoie(
        label_origin="",
        label_raw="",
        label_preproc=["ART", "ANCIENNE", "RUE", "TOULOUSE"],
        types_and_positions={
            "RUE": (2, 3),
            "ANCIENNE": (1, 1),
        },
    )
    position_start_min = 1
    position_end_min = 2
    # When
    result = use_case().execute(infovoie, position_start_min, position_end_min)
    # Then
    assert result.label_preproc == ["ART", "TOULOUSE"]
    assert "RUE" in result.types_and_positions
    assert "ANCIENNE" in result.types_and_positions
    assert result.types_and_positions["RUE"] == (2, 3)
