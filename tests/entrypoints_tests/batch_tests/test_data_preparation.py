import pandas as pd
from decoupage_libelles.entrypoints.batch.data_preparation import build_voie_column, filter_majic


# ---------------------------------------------------------------------------
# build_voie_column
# ---------------------------------------------------------------------------

def test_une_seule_colonne_retournee_directement():
    # Given
    df = pd.DataFrame({"nom_voie": ["RUE HOCHE", "AVENUE VERDIER"]})
    # When
    result_df, col = build_voie_column(df, ["nom_voie"])
    # Then — pas de colonne créée, col = nom original
    assert col == "nom_voie"
    assert "nomVoieComplete" not in result_df.columns


def test_plusieurs_colonnes_concatenees():
    # Given
    df = pd.DataFrame({"type": ["RUE", "AVENUE"], "nom": ["HOCHE", "VERDIER"]})
    # When
    result_df, col = build_voie_column(df, ["type", "nom"])
    # Then
    assert col == "nomVoieComplete"
    assert result_df["nomVoieComplete"].tolist() == ["RUE HOCHE", "AVENUE VERDIER"]


def test_espaces_superflus_supprimes():
    # Given — valeurs avec espaces multiples après concat
    df = pd.DataFrame({"a": ["RUE  "], "b": ["  HOCHE"]})
    # When
    result_df, _ = build_voie_column(df, ["a", "b"])
    # Then
    assert result_df["nomVoieComplete"].iloc[0] == "RUE HOCHE"


def test_colonne_manquante_ignoree_avec_avertissement(capsys):
    # Given — colonne "manquante" absente du DataFrame
    df = pd.DataFrame({"type": ["RUE"]})
    # When
    result_df, _ = build_voie_column(df, ["type", "manquante"])
    # Then — pas d'erreur, avertissement affiché
    captured = capsys.readouterr()
    assert "manquante" in captured.out


def test_valeurs_nulles_traitees_comme_chaine_vide():
    # Given
    df = pd.DataFrame({"type": ["RUE"], "nom": [None]})
    # When
    result_df, _ = build_voie_column(df, ["type", "nom"])
    # Then — pas d'erreur, None → ""
    assert result_df["nomVoieComplete"].iloc[0] == "RUE"


def test_colonne_cible_personnalisable():
    # Given
    df = pd.DataFrame({"a": ["X"], "b": ["Y"]})
    # When
    result_df, col = build_voie_column(df, ["a", "b"], target_col="maColonne")
    # Then
    assert col == "maColonne"
    assert "maColonne" in result_df.columns


# ---------------------------------------------------------------------------
# filter_majic
# ---------------------------------------------------------------------------

def test_sans_ccodep_dataframe_inchange():
    # Given — pas de colonne ccodep
    df = pd.DataFrame({"nom": ["RUE HOCHE"]})
    # When
    result = filter_majic(df)
    # Then
    assert len(result) == 1
    assert "nom" in result.columns


def test_ccodep_padde_sur_2_caracteres():
    # Given — ccodep = "1" au lieu de "01"
    df = pd.DataFrame({"ccodep": ["1", "75"], "ccocom": ["001", "056"]})
    # When
    result = filter_majic(df)
    # Then
    assert result["ccodep"].tolist() == ["01", "75"]


def test_dom_tom_hors_scope_filtre():
    # Given — DOM 97x avec ccocom commençant par 5 (hors scope)
    df = pd.DataFrame({
        "ccodep": ["97", "97", "75"],
        "ccocom": ["501", "101", "056"],  # 501 → hors scope, 101 → ok, 056 → ok
    })
    # When
    result = filter_majic(df)
    # Then — ligne avec ccocom 501 supprimée
    assert len(result) == 2
    assert "501" not in result["ccocom"].tolist()


def test_colonnes_reordonnees():
    # Given — colonnes dans le désordre
    df = pd.DataFrame({
        "autre": ["x"],
        "ccocom": ["056"],
        "ccodep": ["75"],
        "idl": ["123"],
    })
    # When
    result = filter_majic(df)
    # Then — idl avant ccocom
    cols = list(result.columns)
    assert cols.index("idl") < cols.index("ccocom")
