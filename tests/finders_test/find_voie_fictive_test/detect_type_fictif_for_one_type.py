import unittest
import sys

sys.path.append("../src/decoupage_libelles/")

from informations_on_libelle_voie.model.infovoie import InfoVoie
from finders.find_voie_fictive.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase


# ne marche pas à cause des injectors
class DetectTypeFictifForOneTypeTest(unittest.TestCase):
    def setUp(self):
        self.detect_type_fictif_for_one_type_use_case: DetectTypeFictifForOneTypeUseCase = DetectTypeFictifForOneTypeUseCase()

    def test_detect_type_fictif_for_one_type(self):
        # Given
        voie = InfoVoie(label_raw="RUE A", label_preproc=["RUE", "A"], types_and_positions={("RUE", 1): (0, 0)})
        # When
        voie_treated = self.detect_type_fictif_for_one_type_use_case.execute(voie, ["RUE"])
        # Then
        self.assertEqual(voie, voie_treated)

    def test_detect_type_fictif_for_one_type_no_fictif(self):
        # Given
        voie = InfoVoie(label_raw="RUE HOCHE", label_preproc=["RUE", "HOCHE"], types_and_positions={("RUE", 1): (0, 0)})
        # When
        voie_treated = self.detect_type_fictif_for_one_type_use_case.execute(voie, ["RUE"])
        # Then
        self.assertEqual(None, voie_treated)

    def test_detect_type_fictif_for_one_type_returns_empty_voie(self):
        # Given
        voie = InfoVoie("")
        # When
        voie_treated = self.detect_type_fictif_for_one_type_use_case.execute(voie, ["ALLEE"])
        # Then
        self.assertEqual(voie, voie_treated)


if __name__ == "__main__":
    unittest.main()
