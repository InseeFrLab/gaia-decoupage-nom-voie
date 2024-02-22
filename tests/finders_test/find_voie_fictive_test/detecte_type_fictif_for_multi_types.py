import unittest
import sys

sys.path.append("../src/decoupage_libelles/")

from informations_on_libelle_voie.model.infovoie import InfoVoie
from finders.find_voie_fictive.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypesUseCase


# ne marche pas à cause des injectors
class DetectTypeFictifForMultiTypesTest(unittest.TestCase):
    def setUp(self):
        self.detect_type_fictif_for_multi_types_use_case: DetectTypeFictifForMultiTypesUseCase = DetectTypeFictifForMultiTypesUseCase()

    def test_detect_type_fictif_for_multi_types(self):
        # Given
        voie = InfoVoie(label_raw="RUE HOCHE ALL A", label_preproc=["RUE", "HOCHE", "ALL", "A"], types_and_positions={("RUE", 1): (0, 0), ("ALLEE", 1): (2, 2)})
        # When
        voie_treated = self.detect_type_fictif_for_multi_types_use_case.execute(voie, ["ALLEE"])
        # Then
        self.assertEqual(voie, voie_treated)

    def test_detect_type_fictif_for_multi_types_no_fictif(self):
        # Given
        voie = InfoVoie(label_raw="RUE CORENTIN CELTON RESIDENCE ERNEST RENAN", label_preproc=["RUE", "CORENTIN", "CELTON", "RESIDENCE", "ERNEST", "RENAN"], types_and_positions={("RUE", 1): (0, 0)})
        # When
        voie_treated = self.detect_type_fictif_for_multi_types_use_case.execute(voie, ["ALLEE"])
        # Then
        self.assertEqual(None, voie_treated)

    def test_detect_type_fictif_for_multi_types_returns_empty_voie(self):
        # Given
        voie = InfoVoie("")
        # When
        voie_treated = self.detect_type_fictif_for_multi_types_use_case.execute(voie, ["ALLEE"])
        # Then
        self.assertEqual(voie, voie_treated)


if __name__ == "__main__":
    unittest.main()
