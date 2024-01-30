import unittest
from preprocessors.ponctuation.domain.use_case.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase


class SuppressPonctuationInWordsTest(unittest.TestCase):
    def setUp(self):
        self.suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = SuppressPonctuationInWordsUseCase()

    def test_suppression_ponctuation(self):
        # Given
        chaine_traitee = ["Avenue", "(parentheses)"]
        # When
        liste_mots = self.suppress_ponctuation_in_words_use_case.execute(chaine_traitee, ["(", ")"])
        # Then
        self.assertEqual(["Avenue", "parentheses"], liste_mots)

    def test_suppression_ponctuation_returns_empty_list(self):
        # Given
        chaine_traitee = []
        # When
        liste_mots = self.suppress_ponctuation_in_words_use_case.execute(chaine_traitee, ["(", ")"])
        # Then
        self.assertEqual([], liste_mots)


if __name__ == "__main__":
    unittest.main()
