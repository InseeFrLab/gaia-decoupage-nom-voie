import pandas as pd
from unittest.mock import MagicMock
from decoupage_libelles.entrypoints.batch.parallel_processor import process_chunk, run_parallel


# ---------------------------------------------------------------------------
# process_chunk
# ---------------------------------------------------------------------------

def _api_ok(libelles):
    """Simule une API qui retourne type+lib pour chaque libellé."""
    return [
        {label: {
            "typeVoie": "RUE",
            "libelleVoie": label,
            "complementAdresse": "",
            "complementAdresse2": "",
            "numero": "",
            "indice_rep": ""
        }}
        for label in libelles
    ]


def test_process_chunk_appelle_api_avec_libelles():
    # Given
    chunk = pd.DataFrame({"nom_voie": ["RUE HOCHE", "AVENUE VERDIER"]})
    api_mock = MagicMock(side_effect=_api_ok)
    # When
    process_chunk(chunk, ["nom_voie"], api_mock)
    # Then
    api_mock.assert_called_once_with(["RUE HOCHE", "AVENUE VERDIER"])


def test_process_chunk_joint_resultats_au_chunk():
    # Given
    chunk = pd.DataFrame({"nom_voie": ["RUE HOCHE"]})
    # When
    result = process_chunk(chunk, ["nom_voie"], _api_ok)
    # Then — colonnes résultat ajoutées
    assert "type_voie_parse" in result.columns
    assert "libelle_voie_parse" in result.columns
    assert len(result) == 1


def test_process_chunk_chunk_vide_retourne_inchange():
    # Given — toutes les valeurs nulles
    chunk = pd.DataFrame({"nom_voie": [None, None]})
    api_mock = MagicMock()
    # When
    result = process_chunk(chunk, ["nom_voie"], api_mock)
    # Then — API non appelée
    api_mock.assert_not_called()
    assert len(result) == 2


def test_process_chunk_api_en_erreur_retourne_chunk_original():
    # Given
    chunk = pd.DataFrame({"nom_voie": ["RUE HOCHE"]})
    api_mock = MagicMock(return_value=None)
    # When
    result = process_chunk(chunk, ["nom_voie"], api_mock)
    # Then — chunk retourné sans colonnes supplémentaires
    assert list(result.columns) == ["nom_voie"]


def test_process_chunk_colonnes_numero_indice_supprimees():
    # Given
    chunk = pd.DataFrame({"nom_voie": ["RUE HOCHE"]})
    # When
    result = process_chunk(chunk, ["nom_voie"], _api_ok)
    # Then
    assert "numero" not in result.columns
    assert "indice_rep" not in result.columns


# ---------------------------------------------------------------------------
# run_parallel
# ---------------------------------------------------------------------------

def test_run_parallel_traite_tous_les_chunks():
    # Given — 3 chunks de 1 ligne chacun
    chunks = [
        pd.DataFrame({"nom_voie": ["RUE HOCHE"]}),
        pd.DataFrame({"nom_voie": ["AVENUE VERDIER"]}),
        pd.DataFrame({"nom_voie": ["CHEMIN DES PINS"]}),
    ]
    api_mock = MagicMock(side_effect=_api_ok)
    # When
    result = run_parallel(iter(chunks), len(chunks), ["nom_voie"], api_mock, num_threads=2)
    # Then — 3 lignes dans le résultat final
    assert len(result) == 3
    assert api_mock.call_count == 3


def test_run_parallel_retourne_dataframe_concatene():
    # Given
    chunks = [
        pd.DataFrame({"nom_voie": ["RUE HOCHE"]}),
        pd.DataFrame({"nom_voie": ["AVENUE VERDIER"]}),
    ]
    # When
    result = run_parallel(iter(chunks), 2, ["nom_voie"], _api_ok, num_threads=1)
    # Then — DataFrame fusionné, index réinitialisé
    assert list(result.index) == [0, 1]
