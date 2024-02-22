import unittest

from informations_on_libelle_voie.model.infovoie import InfoVoie
from finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from finders.find_complement.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase


### Comment faire marcehr avec mock ??? car complement finder est appelé dans une boucle (injector ???)
class ApplyComplementFinderOnVoiesTest(unittest.TestCase):
    def setUp(self):
        self.complement_finder_use_case: ComplementFinderUseCase = ComplementFinderUseCase()
        self.apply_complement_finder_on_voies_use_case: ApplyComplementFinderOnVoiesUseCase = ApplyComplementFinderOnVoiesUseCase(self.complement_finder_use_case)

    def test_apply_complement_finder_no_type(self):
        # Given
        voies = [
            InfoVoie(label_raw="LE TILLET BAT A", label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={}),
            InfoVoie(label_raw="LES SEMAPHORES", label_preproc=["LES", "SEMAPHORES"], types_and_positions={}),
        ]
        # When
        voies_treated_compl, voies_target_whitout_compl = self.apply_complement_finder_on_voies_use_case.execute(voies, ["BAT", "IMM"])
        # Then
        voies_target_compl = [InfoVoie(label_raw="LE TILLET BAT A", label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={("BAT", 1): (2, 2)})]
        voies_target_without_compl = [InfoVoie(label_raw="LES SEMAPHORES", label_preproc=["LES", "SEMAPHORES"], types_and_positions={})]
        self.assertEqual(voies_target_compl, voies_treated_compl)
        self.assertEqual(voies_target_without_compl, voies_target_whitout_compl)

    def test_apply_complement_finder_returns_empty_voie(self):
        # Given
        voies = [InfoVoie(""), InfoVoie(""), InfoVoie("")]
        # When
        voies_treated_compl, voies_target_whitout_compl = self.apply_complement_finder_on_voies_use_case.execute(voies, ["BAT"])
        # Then
        self.assertEqual(voies_target_whitout_compl, voies)
        self.assertEqual(voies_treated_compl, [])


if __name__ == "__main__":
    unittest.main()
