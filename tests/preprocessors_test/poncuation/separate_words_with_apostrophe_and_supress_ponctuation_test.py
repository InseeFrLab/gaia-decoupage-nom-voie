import unittest
from typing import List

from preprocessors.ponctuation.separate_words_with_apostrophe_and_supress_ponctuation import SeparateWordsWithApostropheAndSupressPonctuation
from voie_classes.voie import Voie


class SeparateWordsWithApostropheAndSupressPonctuationTest:
    def setUp(self):
        self.separate_pontuation_and_words_with_apostrophe: SeparateWordsWithApostropheAndSupressPonctuation = SeparateWordsWithApostropheAndSupressPonctuation()

    def tester_separate_pontuation_and_words_with_apostrophe(self):
        # Given
        chaine_traitee = Voie(label_raw="HAMEAU L'HERITIER .")
        # When
        liste_mots = self.separate_pontuation_and_words_with_apostrophe.execute(chaine_traitee, ["."])
        # Then
        self.assertEqual(["HAMEAU", "L", "HERITIER"], liste_mots)

    def tester_separate_pontuation_and_words_with_apostrophe_retourne_liste_vide(self):
        # Given
        chaine_traitee = []
        # When
        liste_mots = self.separate_pontuation_and_words_with_apostrophe.execute(chaine_traitee, ["."])
        # Then
        self.assertEqual([], liste_mots)


if __name__ == "__main__":
    unittest.main()