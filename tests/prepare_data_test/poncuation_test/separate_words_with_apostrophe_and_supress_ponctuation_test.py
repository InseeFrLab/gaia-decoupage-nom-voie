import unittest

from prepare_data.ponctuation.domain.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase


class SeparateWordsWithApostropheAndSupressPonctuationTest(unittest.TestCase):
    def setUp(self):
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = SeparateWordsWithApostropheAndSupressPonctuationUseCase()

    def test_separate_pontuation_and_words_with_apostrophe(self):
        # Given
        label_to_treat = "HAMEAU L'HERITIER ."
        # When
        label_treated = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(label_to_treat, ["."])
        # Then
        label_target = ["HAMEAU", "L", "HERITIER"]
        self.assertEqual(label_target, label_treated)

    def test_separate_pontuation_and_words_with_apostrophe_returns_empty_list(self):
        # Given
        label_to_treat = ""
        # When
        label_treated = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(label_to_treat, ["."])
        # Then
        label_target = []
        self.assertEqual(label_target, label_treated)


if __name__ == "__main__":
    unittest.main()