from unittest.mock import MagicMock
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.apply_postagging_use_case import ApplyPostaggingUseCase


def test_execute_with_label_postag():
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three"], label_postag=["l1"])
    # When
    mock_nlp_model_execution = MagicMock()
    result = ApplyPostaggingUseCase(mock_nlp_model_execution).execute(infovoie)
    # Then
    assert result.label_postag == ["l1"]


def test_execute_without_label_postag():
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three"])
    expected_postag = ["1", "2", "3"]
    # When
    mock_nlp_model_execution = MagicMock()
    mock_nlp_model_execution.execute.return_value = [MagicMock(pos_="1"), MagicMock(pos_="2"), MagicMock(pos_="3")]
    result = ApplyPostaggingUseCase(nlp_model_execution=mock_nlp_model_execution).execute(infovoie)
    # Then
    mock_nlp_model_execution.execute.assert_called_once_with("one two three")
    assert result.label_postag == expected_postag
