from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher
from decoupage_libelles.finders.type.model.type_finder_utils import TypeFinderUtils


def _make_voie(nb_types: int) -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = ["RUE", "HOCHE"]
    v.types_and_positions = {(f"TYPE{i}", 1): (0, 0) for i in range(nb_types)}
    return v


def launcher(
    preprocessor=MagicMock(),
    no_type=MagicMock(),
    one_type=MagicMock(),
    two_plus=MagicMock(),
) -> TypeVoieDecoupageLauncher:
    tfu = TypeFinderUtils(type_voie_df=None)
    return TypeVoieDecoupageLauncher(preprocessor, no_type, one_type, two_plus, tfu)


def test_routage_0_type():
    # Given
    voie = _make_voie(0)
    prep_mock = MagicMock(); prep_mock.execute.return_value = [voie]
    no_type_mock = MagicMock(); no_type_mock.execute.return_value = ["result_0"]
    one_type_mock = MagicMock()
    two_plus_mock = MagicMock()
    # When
    res = launcher(prep_mock, no_type_mock, one_type_mock, two_plus_mock).execute(["LES HARDONNIERES"])
    # Then
    no_type_mock.execute.assert_called_once_with([voie])
    one_type_mock.execute.assert_not_called()
    two_plus_mock.execute.assert_not_called()
    assert res == ["result_0"]


def test_routage_1_type():
    # Given
    voie = _make_voie(1)
    prep_mock = MagicMock(); prep_mock.execute.return_value = [voie]
    no_type_mock = MagicMock()
    one_type_mock = MagicMock(); one_type_mock.execute.return_value = ["result_1"]
    two_plus_mock = MagicMock()
    # When
    res = launcher(prep_mock, no_type_mock, one_type_mock, two_plus_mock).execute(["CHE DES SEMAPHORES"])
    # Then
    no_type_mock.execute.assert_not_called()
    one_type_mock.execute.assert_called_once_with([voie])
    two_plus_mock.execute.assert_not_called()
    assert res == ["result_1"]


def test_routage_2_types():
    # Given
    voie = _make_voie(2)
    prep_mock = MagicMock(); prep_mock.execute.return_value = [voie]
    no_type_mock = MagicMock()
    one_type_mock = MagicMock()
    two_plus_mock = MagicMock(); two_plus_mock.execute.return_value = ["result_2"]
    # When
    res = launcher(prep_mock, no_type_mock, one_type_mock, two_plus_mock).execute(["RUE HOCHE AVENUE VERDIER"])
    # Then
    two_plus_mock.execute.assert_called_once_with([voie])
    no_type_mock.execute.assert_not_called()
    one_type_mock.execute.assert_not_called()
    assert res == ["result_2"]


def test_routage_mixte():
    # Given — 3 voies avec 0, 1 et 2 types
    v0 = _make_voie(0); v1 = _make_voie(1); v2 = _make_voie(2)
    prep_mock = MagicMock(); prep_mock.execute.return_value = [v0, v1, v2]
    no_type_mock = MagicMock(); no_type_mock.execute.return_value = ["r0"]
    one_type_mock = MagicMock(); one_type_mock.execute.return_value = ["r1"]
    two_plus_mock = MagicMock(); two_plus_mock.execute.return_value = ["r2"]
    # When
    res = launcher(prep_mock, no_type_mock, one_type_mock, two_plus_mock).execute(["a", "b", "c"])
    # Then — chaque handler reçoit la bonne liste
    no_type_mock.execute.assert_called_once_with([v0])
    one_type_mock.execute.assert_called_once_with([v1])
    two_plus_mock.execute.assert_called_once_with([v2])
    assert set(res) == {"r0", "r1", "r2"}


def test_liste_vide():
    # Given
    prep_mock = MagicMock(); prep_mock.execute.return_value = []
    no_mock = MagicMock(); one_mock = MagicMock(); two_mock = MagicMock()
    # When
    res = launcher(prep_mock, no_mock, one_mock, two_mock).execute([])
    # Then — aucun handler appelé
    no_mock.execute.assert_not_called()
    one_mock.execute.assert_not_called()
    two_mock.execute.assert_not_called()
    assert res == []


def test_preprocessing_appele_avec_type_finder_utils():
    # Given — vérifier que le TypeFinderUtils est bien passé au preprocesseur
    voie = _make_voie(1)
    prep_mock = MagicMock(); prep_mock.execute.return_value = [voie]
    one_mock = MagicMock(); one_mock.execute.return_value = []
    tfu_mock = MagicMock()
    lnch = TypeVoieDecoupageLauncher(prep_mock, MagicMock(), one_mock, MagicMock(), tfu_mock)
    # When
    lnch.execute(["CHE DES SEMAPHORES"])
    # Then — le preprocesseur reçoit bien le TypeFinderUtils
    call_args = prep_mock.execute.call_args
    assert call_args[0][1] is tfu_mock


def test_infos_voie_creees_pour_chaque_libelle():
    # Given
    prep_mock = MagicMock()
    captured_voies = []
    def capture(voies, tfu):
        captured_voies.extend(voies)
        for v in voies:
            v.types_and_positions = {}
        return voies
    prep_mock.execute.side_effect = capture
    no_mock = MagicMock(); no_mock.execute.return_value = []
    tfu = TypeFinderUtils(type_voie_df=None)
    lnch = TypeVoieDecoupageLauncher(prep_mock, no_mock, MagicMock(), MagicMock(), tfu)
    # When
    lnch.execute(["RUE HOCHE", "AVENUE VERDIER", "CHEMIN DES PINS"])
    # Then — 3 InfoVoie créées avec le bon label_origin
    assert len(captured_voies) == 3
    assert captured_voies[0].label_origin == "RUE HOCHE"
    assert captured_voies[2].label_origin == "CHEMIN DES PINS"
