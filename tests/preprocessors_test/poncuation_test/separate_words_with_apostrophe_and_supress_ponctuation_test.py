import unittest
from typing import List

from preprocessors.ponctuation.domain.use_case.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from voie_classes.voie import Voie


class SeparateWordsWithApostropheAndSupressPonctuationTest:
    def setUp(self):
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = SeparateWordsWithApostropheAndSupressPonctuationUseCase()

    def test_separate_pontuation_and_words_with_apostrophe(self):
        # Given
        chaine_traitee = Voie(label_raw="HAMEAU L'HERITIER .")
        # When
        liste_mots = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(chaine_traitee, ["."])
        # Then
        self.assertEqual(["HAMEAU", "L", "HERITIER"], liste_mots)

    def test_separate_pontuation_and_words_with_apostrophe_returns_empty_list(self):
        # Given
        chaine_traitee = []
        # When
        liste_mots = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(chaine_traitee, ["."])
        # Then
        self.assertEqual([], liste_mots)


if __name__ == "__main__":
    unittest.main()