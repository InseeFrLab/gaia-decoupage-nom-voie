from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.apply_postagging_use_case import ApplyPostaggingUseCase


def test_execute_with_label_postag(mocker):
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three"], label_postag=["l1"])
    # When
    result = ApplyPostaggingUseCase(nlp_model_execution=mocker.Mock()).execute(infovoie)
    # Then
    assert result.label_postag == ["l1"]


def test_execute_without_label_postag(mocker):
    # Given
    infovoie = InfoVoie(label_preproc=["one", "two", "three"])
    expected_postag = ["1", "2", "3"]
    # When
    mock_nlp_model = mocker.Mock()
    mock_nlp_model.execute.return_value = [mocker.Mock(pos_="1"), mocker.Mock(pos_="2"), mocker.Mock(pos_="3")]
    result = ApplyPostaggingUseCase(nlp_model_execution=mock_nlp_model).execute(infovoie)
    # Then
    mock_nlp_model.execute.assert_called_once_with("one two three")
    assert result.label_postag == expected_postag
