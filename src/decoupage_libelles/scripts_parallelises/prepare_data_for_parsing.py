import re


def create_voie_column(df, column_names, nom_col_name="nomVoieComplete"):
    """
    Crée une colonne de nom de voie complet dans le DataFrame en combinant les colonnes spécifiées.

    :param df: DataFrame dans lequel ajouter la colonne d'adresse.
    :param nom_col_name: Nom de la colonne de voie à créer, par défaut "nomVoieComplete".
    :param column_names: Liste des noms des colonnes à combiner dans l'ordre pour créer le nom de voie complet.
    """
    if len(column_names) > 1:
        # Initialisation de la colonne d'adresse avec une chaîne vide
        df[nom_col_name] = ''
        # Parcours des noms de colonnes fournies
        for column in column_names:
            if column in df.columns:
                df[nom_col_name] += df[column].fillna('').astype(str) + ' '
            else:
                print(f"Attention : La colonne '{column}' n'existe pas dans le DataFrame.")

        # Enlever les espaces superflus à la fin
        df[nom_col_name] = df[nom_col_name].apply(lambda x: re.sub(r'\s+', ' ', x).strip())
        return df, nom_col_name

    else:
        return df, column_names[0]
