import unittest
from unittest.mock import Mock

from preprocessors.ponctuation.domain.use_case.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from preprocessors.ponctuation.domain.use_case.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from preprocessors.ponctuation.domain.use_case.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase
from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib


class PonctuationPreprocessorTest(unittest.TestCase):
    def setUp(self):
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = Mock()
        self.suppress_ponctuation_in_words_use_case: PonctuationPreprocessorUseCase = Mock()
        self.ponctuation_preprocessor_use_case = PonctuationPreprocessorUseCase(self.separate_pontuation_and_words_with_apostrophe, self.suppress_ponctuation_in_words)

    def test_preprocessor_calls_different_services(self):
        # Given
        voie_obj = Voie(label_raw="libelle")
        ponctuations = []
        self.suppress_ponctuation_in_words_use_case.execute.return_value = []
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute.return_value = []
        # When
        voie = self.ponctuation_preprocessor_use_case.execute(voie_obj, ponctuations)
        # Then
        self.assertEqual(InfoLib([]), voie.infolib)
        self.suppress_ponctuation_in_words_use_case.execute.assert_called_once()
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
