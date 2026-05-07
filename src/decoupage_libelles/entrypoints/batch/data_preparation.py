"""
Préparation des colonnes d'entrée avant découpage.
"""
import re
import pandas as pd
from typing import List, Tuple


def build_voie_column(df: pd.DataFrame, column_names: List[str], target_col: str = "nomVoieComplete") -> Tuple[pd.DataFrame, str]:
    """
    Construit la colonne de libellé de voie à découper.

    Si une seule colonne est fournie, elle est utilisée directement.
    Si plusieurs colonnes sont fournies, elles sont concaténées avec un espace.

    Retourne le DataFrame modifié et le nom de la colonne de voie.
    """
    if len(column_names) == 1:
        return df, column_names[0]

    df[target_col] = ""
    for col in column_names:
        if col in df.columns:
            df[target_col] += df[col].fillna("").astype(str) + " "
        else:
            print(f"Attention : la colonne '{col}' est absente du DataFrame.")

    df[target_col] = df[target_col].apply(lambda x: re.sub(r"\s+", " ", x).strip())
    return df, target_col


def filter_majic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Post-traitement spécifique aux fichiers MAJIC :
    - Pad de ccodep sur 2 caractères
    - Réordonnement des colonnes
    - Suppression des lignes DOM-TOM hors scope
    """
    if "ccodep" not in df.columns:
        return df

    colonnes_ordre = ["idl", "dnvoiri", "dindic", "dvoilib", "ccoriv", "ccodep", "ccocom", "parcelle"]
    df["ccodep"] = df["ccodep"].astype(str).str.zfill(2)

    cols_presentes = [c for c in colonnes_ordre if c in df.columns]
    cols_restantes = [c for c in df.columns if c not in cols_presentes]
    df = df[cols_presentes + cols_restantes]

    mask = (
        ((df["ccodep"] == "97") & df["ccocom"].astype(str).str[0].isin(["1", "2", "3", "4", "6"]))
        | (df["ccodep"] != "97")
    )
    return df[mask]
