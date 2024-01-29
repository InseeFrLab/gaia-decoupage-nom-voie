import unittest
from unittest.mock import Mock

from preprocessors.ponctuation.ponctuation_preprocessor import PonctuationPreprocessor
from preprocessors.ponctuation.separate_words_with_apostrophe_and_supress_ponctuation import SeparateWordsWithApostropheAndSupressPonctuation
from preprocessors.ponctuation.suppress_ponctuation_in_words import SuppressPonctuationInWords
from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib


class TestPonctuationPreprocessor(unittest.TestCase):
    def setUp(self):
        self.separate_words_with_apostrophe_and_supress_ponctuation: SeparateWordsWithApostropheAndSupressPonctuation = Mock()
        self.suppress_ponctuation_in_words: SuppressPonctuationInWords = Mock()
        self.ponctuation_preprocessor = PonctuationPreprocessor(self.separate_pontuation_and_words_with_apostrophe, self.suppress_ponctuation_in_words)

    def tester_preprocessor_appelle_differents_services(self):
        # Given
        voie_obj = Voie(label_raw="libelle")
        ponctuations = []
        self.suppress_ponctuation_in_words.execute.return_value = []
        self.separate_words_with_apostrophe_and_supress_ponctuation.execute.return_value = []
        # When
        voie = self.ponctuation_preprocessor.execute(voie_obj, ponctuations)
        # Then
        self.assertEqual(InfoLib([]), voie.infolib)
        self.suppress_ponctuation_in_words.execute.assert_called_once()
        self.separate_words_with_apostrophe_and_supress_ponctuation.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
