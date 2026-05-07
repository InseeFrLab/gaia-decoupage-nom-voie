from unittest.mock import MagicMock

import pandas as pd

from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.prepare_data.ponctuation.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import GenerateTypeFinderUtilsUseCase


def use_case(
    ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = MagicMock(),
) -> GenerateTypeFinderUtilsUseCase:
    return GenerateTypeFinderUtilsUseCase(ponctuation_preprocessor_use_case)


def _mock_preprocessor(mapping: dict) -> MagicMock:
    """
    Mock du preprocesseur : lit label_origin (1er arg positionnel de InfoVoie)
    pour retourner la valeur correspondante dans le mapping.
    """
    def side_effect(infovoie):
        key = infovoie.label_origin
        infovoie.label_preproc = mapping.get(key, key.upper().split() if key else [])
        return infovoie
    mock = MagicMock()
    mock.execute.side_effect = side_effect
    return mock


def _df(*rows) -> pd.DataFrame:
    """Crée un DataFrame LIBELLE_CANONIQUE/VARIANTE à partir de tuples (canonique, variante)."""
    return pd.DataFrame(rows, columns=["LIBELLE_CANONIQUE", "VARIANTE"])


def test_canoniques_extraits():
    # Given — le CSV contient AVENUE et RUE
    df = _df(("AVENUE", "AV"), ("AVENUE", "AVENUE"), ("RUE", "R"), ("RUE", "RUE"))
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVENUE": ["AVENUE"], "R": ["R"], "RUE": ["RUE"]})
    type_finder_utils = TypeFinderUtils(type_voie_df=df)
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert "AVENUE" in res.canoniques
    assert "RUE" in res.canoniques


def test_variante2canonique_depuis_csv():
    # Given
    df = _df(("AVENUE", "AV"), ("AVENUE", "AVE"), ("AVENUE", "AVENUE"))
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVE": ["AVE"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils(type_voie_df=df)
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert res.variante2canonique["AV"] == "AVENUE"
    assert res.variante2canonique["AVE"] == "AVENUE"


def test_canonique_se_reconnait_lui_meme_via_csv():
    # Given — la ligne AVENUE/AVENUE est dans le CSV (plus dans le code)
    df = _df(("AVENUE", "AV"), ("AVENUE", "AVENUE"))
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils(type_voie_df=df)
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert res.variante2canonique["AVENUE"] == "AVENUE"


def test_canonique_absent_du_csv_non_ajoute():
    # Given — la ligne AVENUE/AVENUE est absente du CSV (Option A supprimée)
    df = _df(("AVENUE", "AV"))
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils(type_voie_df=df)
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then — AVENUE n'est pas une variante connue car absent du CSV
    assert "AVENUE" not in res.variante2canonique


def test_variantes_mono_et_multi_separes():
    # Given
    df = _df(
        ("AVENUE", "AV"), ("AVENUE", "AVENUE"),
        ("ANCIEN CHEMIN", "ANC CHEM"), ("ANCIEN CHEMIN", "ANCIEN CHEMIN"),
    )
    preprocessor = _mock_preprocessor({
        "AV": ["AV"], "AVENUE": ["AVENUE"],
        "ANC CHEM": ["ANC", "CHEM"], "ANCIEN CHEMIN": ["ANCIEN", "CHEMIN"],
    })
    type_finder_utils = TypeFinderUtils(type_voie_df=df)
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert "AV" in res.variantes_mono
    assert "AVENUE" in res.variantes_mono
    assert "ANC CHEM" in res.variantes_multi
    assert "ANCIEN CHEMIN" in res.variantes_multi


def test_preprocesseur_appele_pour_chaque_variante():
    # Given — 2 variantes dans le CSV
    df = _df(("AVENUE", "AV"), ("AVENUE", "AVENUE"))
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils(type_voie_df=df)
    # When
    use_case(preprocessor).execute(type_finder_utils)
    # Then — appelé exactement une fois par ligne du CSV
    assert preprocessor.execute.call_count == 2
