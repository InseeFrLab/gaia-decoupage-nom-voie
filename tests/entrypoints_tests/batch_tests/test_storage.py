import pytest
import pandas as pd
from decoupage_libelles.entrypoints.batch.storage import detect_file_type, output_path, save
from decoupage_libelles.entrypoints.batch.storage import connect_s3


# ---------------------------------------------------------------------------
# detect_file_type
# ---------------------------------------------------------------------------

def test_detect_csv():
    assert detect_file_type("data/voies.csv") == "csv"


def test_detect_parquet():
    assert detect_file_type("data/voies.parquet") == "parquet"


def test_detect_dossier_parquet():
    # Given — pas d'extension dans le nom de fichier
    assert detect_file_type("data/voies_dossier") == "dossier_parquet"


def test_detect_extension_inconnue():
    with pytest.raises(ValueError, match="Extension non supportée"):
        detect_file_type("data/voies.xlsx")


# ---------------------------------------------------------------------------
# output_path
# ---------------------------------------------------------------------------

def test_output_path_csv_vers_parquet():
    assert output_path("data/voies.csv", "parquet") == "data/voies_parsed.parquet"


def test_output_path_parquet_vers_csv():
    assert output_path("data/voies.parquet", "csv") == "data/voies_parsed.csv"


def test_output_path_dossier_parquet():
    assert output_path("data/voies_dossier", "parquet") == "data/voies_dossier_parsed.parquet"


def test_output_path_s3():
    assert output_path("s3://bucket/dir/voies.csv", "parquet") == "s3://bucket/dir/voies_parsed.parquet"


# ---------------------------------------------------------------------------
# save — local
# ---------------------------------------------------------------------------

def test_save_csv_local(tmp_path):
    # Given
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    path = str(tmp_path / "out.csv")
    # When
    save(df, path, output_format="csv", sep=",", encoding="utf-8", fs=None)
    # Then
    result = pd.read_csv(path)
    assert list(result.columns) == ["a", "b"]
    assert len(result) == 2


def test_save_parquet_local(tmp_path):
    # Given
    df = pd.DataFrame({"a": [1, 2]})
    path = str(tmp_path / "out.parquet")
    # When
    save(df, path, output_format="parquet", sep=",", encoding="utf-8", fs=None)
    # Then
    result = pd.read_parquet(path)
    assert len(result) == 2


def test_save_format_inconnu(tmp_path):
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError, match="Format non reconnu"):
        save(df, str(tmp_path / "out.xyz"), output_format="xlsx", sep=",", encoding="utf-8")


# ---------------------------------------------------------------------------
# connect_s3
# ---------------------------------------------------------------------------

def test_connect_s3_plateforme_inconnue():
    with pytest.raises(ValueError, match="Plateforme inconnue"):
        connect_s3("azure")
