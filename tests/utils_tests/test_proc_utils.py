import unittest
import sys
sys.path.append('../src')

from utils.proc_utils import (find_type_complement,
                              find_voies_fictives)
from constants.constant_lists import (liste_types_complement_1,
                                      liste_voie_fictive_2)
from processing.decoupage_voie import DecoupageVoie


class TestPreprocUtils(unittest.TestCase):
    def test_find_voies_compl(self):
        test_voie = DecoupageVoie("IMM ERNEST RENAN RUE DES LYS",
                                  ['IMM', 'ERNEST', 'RENAN', 'RUE', 'DES', 'LYS'],
                                  ['RUE'],
                                  [3],
                                  None,
                                  None,)

        result_voie = DecoupageVoie("IMM ERNEST RENAN RUE DES LYS",
                                    ['IMM', 'ERNEST', 'RENAN', 'RUE', 'DES', 'LYS'],
                                    ['IMM', 'RUE'],
                                    [0, 3],
                                    None,
                                    None,)

        self.assertEqual(find_type_complement(test_voie, liste_types_complement_1),
                         result_voie)

    def test_find_voies_fictives_quand_find_trouve_voies_fictives_retourne_voie(self):  # when_context_should_return
        test_voie = DecoupageVoie("RESIDENCE DES CARMES ALLEE 2",
                                  ['RESIDENCE', 'DES', 'CARMES', 'ALLEE', '2'],
                                  ['RESIDENCE', 'ALLEE'],
                                  [0, 3],
                                  None,
                                  None,)
        result_voie = test_voie

        self.assertEqual(find_voies_fictives(test_voie, liste_voie_fictive_2),
                         result_voie)


if __name__ == '__main__':
    unittest.main()
