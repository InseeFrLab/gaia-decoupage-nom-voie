import unittest
from unittest.mock import Mock

from preprocessors.ponctuation.ponctuation_preprocessor import PonctuationPreprocessor
from preprocessors.ponctuation.separate_words_with_apostrophe_and_suppress_ponctuation import SeparateWordsWithApostropheAndSuppressPonctuation
from preprocessors.ponctuation.suppress_ponctuation_in_words import SuppressPonctuationInWords
from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib
from constants.constant_lists import ponctuations


class TestPonctuationPreprocessor(unittest.TestCase):
    def setUp(self):
        self.separate_words_with_apostrophe_and_suppress_ponctuation: SeparateWordsWithApostropheAndSuppressPonctuation = Mock()
        self.suppress_ponctuation_in_words: SuppressPonctuationInWords = Mock()
        self.ponctuation_preprocessor = PonctuationPreprocessor(self.separate_words_with_apostrophe_and_suppress_ponctuation, self.suppress_ponctuation_in_words)

    def tester_preprocessor_appelle_differents_services(self):
        # Given
        voie_obj = Voie(label_raw="VC  L'ESPACE VERT ( SAINT-AUBIN )")
        self.separate_words_with_apostrophe_and_suppress_ponctuation.execute.return_value = ['VC', 'L', 'ESPACE', 'VERT', 'SAINT-AUBIN']
        # question : c'est la return value si on excute la fonction sur la return value de la première foction ? 
        self.suppress_ponctuation_in_words.execute.return_value = ['VC', 'L', 'ESPACE', 'VERT', 'SAINT', 'AUBIN']
        # When
        voie = self.ponctuation_preprocessor.execute(voie_obj, ponctuations)
        # Then
        self.assertEqual(InfoLib(['VC', 'L', 'ESPACE', 'VERT', 'SAINT', 'AUBIN']), voie.infolib)
        self.suppress_ponctuation_in_words.execute.assert_called_once()
        self.separate_words_with_apostrophe_and_suppress_ponctuation.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
