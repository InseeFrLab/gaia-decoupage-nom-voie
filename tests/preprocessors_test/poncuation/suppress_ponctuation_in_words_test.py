import unittest
from preprocessors.ponctuation.suppress_ponctuation_in_words import SuppressPonctuationInWords


class SuppressPonctuationInWordsTest(unittest.TestCase):
    def setUp(self):
        self.suppress_ponctuation_in_words: SuppressPonctuationInWords = SuppressPonctuationInWords()

    def tester_suppression_ponctuation(self):
        # Given
        chaine_traitee = ["Avenue", "(parentheses)"]
        # When
        liste_mots = self.suppress_ponctuation_in_words.execute(chaine_traitee, ["(", ")"])
        # Then
        self.assertEqual(["Avenue", "parentheses"], liste_mots)

    def tester_suppression_ponctuation_retourne_liste_vide(self):
        # Given
        chaine_traitee = []
        # When
        liste_mots = self.suppress_ponctuation_in_words.execute(chaine_traitee, ["(", ")"])
        # Then
        self.assertEqual([], liste_mots)


if __name__ == "__main__":
    unittest.main()
