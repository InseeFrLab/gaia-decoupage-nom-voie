import unittest

from informations_on_libelle_voie.model.infovoie import InfoVoie
from finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase


class ComplementFinderTest(unittest.TestCase):
    def setUp(self):
        self.complement_finder_use_case: ComplementFinderUseCase = ComplementFinderUseCase()

    def test_complement_finder_no_type(self):
        # Given
        voie = InfoVoie(label_raw="LE TILLET BAT A", label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={})
        # When
        voie_treated = self.complement_finder_use_case.execute(voie, ["BAT"])
        # Then
        voie_target = InfoVoie(label_raw="LE TILLET BAT A", label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={("BAT", 1): (2, 2)})
        self.assertEqual(voie_target, voie_treated)

    def test_complement_finder_one_type(self):
        # Given
        voie = InfoVoie(label_raw="IMM L ANJOU AVE DE VLAMINC", label_preproc=["IMM", "L", "ANJOU", "AVE", "DE", "VLAMINC"], types_and_positions={("AVE", 1): (3, 3)})
        # When
        voie_treated = self.complement_finder_use_case.execute(voie, ["IMM"])
        # Then
        voie_target = InfoVoie(label_raw="IMM L ANJOU AVE DE VLAMINC", label_preproc=["IMM", "L", "ANJOU", "AVE", "DE", "VLAMINC"], types_and_positions={("IMM", 1): (0, 0), ("AVE", 1): (3, 3)})
        self.assertEqual(voie_target, voie_treated)

    def test_complement_finder_returns_empty_voie(self):
        # Given
        voie = InfoVoie("")
        # When
        voie_treated = self.complement_finder_use_case.execute(voie, ["BAT"])
        # Then
        self.assertEqual(voie_treated, voie_treated)


if __name__ == "__main__":
    unittest.main()
