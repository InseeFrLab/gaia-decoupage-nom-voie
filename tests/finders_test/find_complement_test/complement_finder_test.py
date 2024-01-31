import unittest
import sys
sys.path.append('../src/decoupage_libelles/')

from voie_classes.decoupage_voie import DecoupageVoie
from voie_classes.informations_on_libelle import InfoLib
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase


class ComplementFinderTest:
    def setUp(self):
        self.complement_finder_use_case: ComplementFinderUseCase = ComplementFinderUseCase()

    def test_complement_finder_no_type(self):
        # Given
        infolib = InfoLib(label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={})
        voie = DecoupageVoie(label_raw="LE TILLET BAT A", infolib=infolib)
        # When
        voie_traited = self.complement_finder_use_case.execute(voie, ["BAT"])
        # Then
        self.assertEqual({('BAT', 1): (2, 2)}, voie_traited.infolib.types_and_positions)

    def test_complement_finder_one_type(self):
        # Given
        infolib = InfoLib(label_preproc=["IMM", "L", "ANJOU", "AVE", "DE", "VLAMINC"], types_and_positions={("AVE", 1): (3, 3)})
        voie = DecoupageVoie(label_raw="IMM L ANJOU AVE DE VLAMINC", infolib=infolib)
        # When
        voie_traited = self.complement_finder_use_case.execute(voie, ["IMM"])
        # Then
        self.assertEqual({("IMM", 1): (0, 0), ("AVE", 1): (3, 3)}, voie_traited.infolib.types_and_positions)

    def test_complement_finder_returns_empty_list(self):
        # Given
        voie = []
        # When
        voie_traited = self.complement_finder_use_case.execute(voie, ["BAT"])
        # Then
        self.assertEqual([], voie_traited)


if __name__ == "__main__":
    unittest.main()