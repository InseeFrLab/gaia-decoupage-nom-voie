import unittest
from unittest.mock import Mock

from prepare_data.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from prepare_data.ponctuation.domain.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from prepare_data.ponctuation.domain.usecase.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie

class PonctuationPreprocessorTest(unittest.TestCase):
    def setUp(self):
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = Mock()
        self.suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = Mock()
        self.ponctuation_preprocessor_use_case = PonctuationPreprocessorUseCase(self.separate_words_with_apostrophe_and_supress_ponctuation_use_case, self.suppress_ponctuation_in_words_use_case)

    def test_preprocessor_calls_different_services(self):
        # Given
        voie_obj = InfoVoie(label_raw="libelle")
        self.suppress_ponctuation_in_words_use_case.execute.return_value = ["libelle"]
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute.return_value = ["libelle"]
        # When
        voie = self.ponctuation_preprocessor_use_case.execute(voie_obj)
        # Then
        voie_target = InfoVoie(label_raw="libelle", label_preproc=["libelle"])
        self.assertEqual(voie_target, voie)
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute.assert_called_once()
        self.suppress_ponctuation_in_words_use_case.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
