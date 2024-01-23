import unittest
import sys
sys.path.append('../src')

from utils.preproc_utils import ponctuation_preproc
from constants.constant_lists import ponctuations
from preprocessing.voie_preprocessed import Voie


class TestPreprocUtils(unittest.TestCase):
    def test_ponctuation_preproc(self):
        test_voie = Voie("HAMEAU L'HERITIER")
        result_voie = Voie("HAMEAU L'HERITIER", ['HAMEAU', 'L', 'HERITIER'])

        self.assertEqual(ponctuation_preproc(test_voie, ponctuations),
                         result_voie)


if __name__ == '__main__':
    unittest.main()
