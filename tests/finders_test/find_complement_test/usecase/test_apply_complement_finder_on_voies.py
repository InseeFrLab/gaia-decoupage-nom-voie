from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.finders.find_complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase
from unittest.mock import MagicMock


def use_case(complement_finder_use_case: ComplementFinderUseCase = MagicMock()) -> ApplyComplementFinderOnVoiesUseCase:
    return ApplyComplementFinderOnVoiesUseCase(complement_finder_use_case=complement_finder_use_case)


def test_execute_aucun_complement_trouve():
    # Given
    voies_obj = [InfoVoie(), InfoVoie(), InfoVoie()]
    types_to_detect = ["type1", "type2"]
    complement_finder_use_case_mock = MagicMock(spec=ComplementFinderUseCase)
    complement_finder_use_case_mock.execute.return_value = None
    # When
    use_case = ApplyComplementFinderOnVoiesUseCase(complement_finder_use_case_mock)
    result = use_case.execute(voies_obj, types_to_detect)
    # Then
    assert result == ([], voies_obj)


def test_execute_complement_trouve():
    # Given
    voies_obj = [InfoVoie(), InfoVoie(), InfoVoie()]
    types_to_detect = ["type1", "type2"]
    complement_finder_use_case_mock = MagicMock(spec=ComplementFinderUseCase)
    complement_finder_use_case_mock.execute.return_value = InfoVoie()
    # When
    use_case = ApplyComplementFinderOnVoiesUseCase(complement_finder_use_case_mock)
    result = use_case.execute(voies_obj, types_to_detect)
    # Then
    assert result == ([InfoVoie(), InfoVoie(), InfoVoie()], [])
