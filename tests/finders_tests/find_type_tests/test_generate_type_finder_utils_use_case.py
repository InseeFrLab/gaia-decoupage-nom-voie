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
    """Crée un mock du preprocesseur qui retourne label_preproc selon le mapping fourni."""
    def side_effect(infovoie):
        infovoie.label_preproc = mapping.get(infovoie.label_origin, infovoie.label_origin.upper().split())
        return infovoie
    mock = MagicMock()
    mock.execute.side_effect = side_effect
    return mock


def test_canoniques_extraits():
    # Given
    preprocessor = _mock_preprocessor({"AV": ["AV"], "RUE": ["RUE"], "AVENUE": ["AVENUE"], "R": ["R"]})
    type_finder_utils = TypeFinderUtils()
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert "AVENUE" in res.canoniques
    assert "RUE" in res.canoniques


def test_variante2canonique_depuis_csv():
    # Given
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVE": ["AVE"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils()
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert res.variante2canonique["AV"] == "AVENUE"
    assert res.variante2canonique["AVE"] == "AVENUE"


def test_option_a_canonique_se_reconnait_lui_meme():
    # Given
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils()
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert res.variante2canonique["AVENUE"] == "AVENUE"


def test_variantes_mono_et_multi_separes():
    # Given
    preprocessor = _mock_preprocessor({
        "AV": ["AV"], "ANC CHEM": ["ANC", "CHEM"],
        "AVENUE": ["AVENUE"], "ANCIEN CHEMIN": ["ANCIEN", "CHEMIN"],
    })
    type_finder_utils = TypeFinderUtils()
    # When
    res = use_case(preprocessor).execute(type_finder_utils)
    # Then
    assert "AV" in res.variantes_mono
    assert "AVENUE" in res.variantes_mono
    assert "ANC CHEM" in res.variantes_multi
    assert "ANCIEN CHEMIN" in res.variantes_multi


def test_preprocesseur_appele_pour_chaque_variante_et_canonique():
    # Given
    preprocessor = _mock_preprocessor({"AV": ["AV"], "AVENUE": ["AVENUE"]})
    type_finder_utils = TypeFinderUtils()
    # When
    use_case(preprocessor).execute(type_finder_utils)
    # Then — appelé au moins une fois par variante + une fois par canonique
    assert preprocessor.execute.call_count >= 2
