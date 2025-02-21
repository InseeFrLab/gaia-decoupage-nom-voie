from unittest.mock import MagicMock

from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_voie_fictive.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


def test_execute_voie_fictive():
    # Given
    voie = InfoVoie()
    liste_voie_commun = ["RUE", "AVENUE"]
    liste_fictive = ["A", "B", "C"]
    generate_information_on_type_ordered_use_case_mock = MagicMock(spec=GenerateInformationOnTypeOrderedUseCase)
    generate_information_on_type_ordered_use_case_mock.execute.return_value = InformationOnTypeOrdered(
        type_name="RUE",
        is_in_penultimate_position=True,
        word_before="B",
        word_after="C",
        occurence=1,
        order_in_lib=0,
        position_start=0,
        position_end=0,
    )
    # When
    use_case = DetectTypeFictifForOneTypeUseCase(generate_information_on_type_ordered_use_case_mock)
    result = use_case.execute(voie, liste_voie_commun, liste_fictive)
    # Then
    assert result == voie


def test_execute_pas_voie_fictive():
    # Given
    voie = InfoVoie()
    liste_voie_commun = ["RUE", "AVENUE"]
    liste_fictive = ["A", "B", "C"]
    generate_information_on_type_ordered_use_case_mock = MagicMock(spec=GenerateInformationOnTypeOrderedUseCase)
    generate_information_on_type_ordered_use_case_mock.execute.return_value = InformationOnTypeOrdered(
        type_name="RUE",
        is_in_penultimate_position=True,
        word_before="D",
        word_after="E",
        occurence=1,
        order_in_lib=0,
        position_start=0,
        position_end=0,
    )
    # When
    use_case = DetectTypeFictifForOneTypeUseCase(generate_information_on_type_ordered_use_case_mock)
    result = use_case.execute(voie, liste_voie_commun, liste_fictive)
    # Then
    assert result is None
