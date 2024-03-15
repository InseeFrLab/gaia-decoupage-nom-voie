from unittest.mock import MagicMock
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_voie_fictive.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypesUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


def test_execute_voie_fictive():
    # Given
    voie = InfoVoie(
        label_origin="LES TILLETS RUE A",
        label_raw="LES TILLETS RUE A",
        label_preproc=["LES", "TILLETS", "RUE", "A"],
        types_and_positions={("RUE", 1): (2, 2)},
        types_detected=["RUE"],
    )
    liste_voie_commun = ["RUE"]
    liste_fictive = ["A", "B", "C"]
    generate_information_on_type_ordered_use_case_mock = MagicMock(spec=GenerateInformationOnTypeOrderedUseCase)
    generate_information_on_type_ordered_use_case_mock.execute.return_value = InformationOnTypeOrdered(
        type_name="RUE",
        is_in_penultimate_position=True,
        word_before=None,
        word_after=None,
        occurence=1,
        position_start=2,
        position_end=2,
        order_in_lib=1,
    )
    get_words_between_use_case_mock = MagicMock(spec=GetWordsBetweenUseCase)
    get_words_between_use_case_mock.execute.return_value = "A"
    # When
    use_case = DetectTypeFictifForMultiTypesUseCase(generate_information_on_type_ordered_use_case_mock, get_words_between_use_case_mock)
    result = use_case.execute(voie, liste_voie_commun, liste_fictive)
    # Then
    assert result == voie


def test_execute_pas_voie_fictive():
    # Given
    voie = InfoVoie()
    voie.types_detected = ["AVENUE"]
    liste_voie_commun = ["RUE"]
    liste_fictive = ["A", "B", "C"]
    generate_information_on_type_ordered_use_case_mock = MagicMock(spec=GenerateInformationOnTypeOrderedUseCase)
    get_words_between_use_case_mock = MagicMock(spec=GetWordsBetweenUseCase)
    # When
    use_case = DetectTypeFictifForMultiTypesUseCase(generate_information_on_type_ordered_use_case_mock, get_words_between_use_case_mock)
    result = use_case.execute(voie, liste_voie_commun, liste_fictive)
    # Then
    assert result is None
