from unittest.mock import MagicMock

from decoupage_libelles.prepare_data.ponctuation.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


def test_preprocessor_calls_different_services():
    # Given
    voie_obj = InfoVoie(label_origin="libelle", label_raw="libelle")
    mock_suppress_ponctuation_in_words_use_case = MagicMock(spec=SuppressPonctuationInWordsUseCase)
    mock_suppress_ponctuation_in_words_use_case.execute.return_value = ["libelle"]
    mock_separate_words_with_apostrophe_and_supress_ponctuation_use_case = MagicMock(spec=SeparateWordsWithApostropheAndSupressPonctuationUseCase)
    mock_separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute.return_value = ["libelle"]
    # When
    ponctuation_preprocessor_use_case = PonctuationPreprocessorUseCase(mock_separate_words_with_apostrophe_and_supress_ponctuation_use_case, mock_suppress_ponctuation_in_words_use_case)
    voie = ponctuation_preprocessor_use_case.execute(voie_obj)
    # Then
    voie_target = InfoVoie(label_origin="libelle", label_raw="libelle", label_preproc=["libelle"])
    assert voie_target == voie
    mock_separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute.assert_called_once()
    mock_suppress_ponctuation_in_words_use_case.execute.assert_called_once()
