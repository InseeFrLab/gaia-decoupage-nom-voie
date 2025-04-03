import pandas as pd
import numpy as np

# source = "majic"
# variables_type_nom_voie = ["dvoilib"]

# source = "ban"
# variables_type_nom_voie = ["nom_voie"]

source = "rca"
variables_type_nom_voie = ['denomination_de_voie_type', 'denomination_de_voie_libelle']

# selectionner 3k lignes sans doublons

df = pd.read_csv(f"C:/Users/FI7L7T/Documents/gaia/voies_echant_{source}.csv")

df = df.drop_duplicates(subset=variables_type_nom_voie)

df = df.iloc[:3000]

df.to_csv(f"C:/Users/FI7L7T/Documents/gaia/voies_echant_{source}.csv", index=False)

# apres avoir parsé les données et retraité les colonnes manuellement
# pour avoir cette structure id_type_voie_query	nom_voie_norm_query	complement_adresse_query	id_type_voie_match1	nom_voie_norm_match1	complement_adresse_match1	id_type_voie_match2	nom_voie_norm_match2	complement_adresse_match2

df = pd.read_csv(f"C:/Users/FI7L7T/Documents/gaia/voies_echant_{source}_parsed.csv")

# Découper en DataFrames de 1000 lignes
df_list = np.array_split(df, np.ceil(len(df) / 1000))

for i, mini_df in enumerate(df_list):
    mini_df.to_csv(f"C:/Users/FI7L7T/Documents/gaia/echant_voies/voies_echant_{source}_{i}.csv", index=False)


# mettre en forme le fichier json annoté

df = pd.read_json("data/voies_echant_ban_2.json")
df.drop(columns=['count'], inplace=True)

df_both = df[df['similarity'] == 'Both accepted'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_both = df_both.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_acc1 = df[df['similarity'] == 'Accepted 1'][['nom_voie_norm_query', 'id_type_voie_match1', 'nom_voie_norm_match1', 'complement_adresse_match1', 'justification']]
df_acc1 = df_acc1.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match1': 'id_type_voie', 'nom_voie_norm_match1': 'nom_voie_norm', 'complement_adresse_match1': 'complement_adresse'})

df_acc2 = df[df['similarity'] == 'Accepted 2'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_acc2 = df_acc2.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_rej = df[df['similarity'] == 'Rejected'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_rej = df_rej.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_indecis = df[df['similarity'] == 'Undecided'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_indecis = df_indecis.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_final = pd.concat([df_both, df_acc1, df_acc2, df_rej, df_indecis], ignore_index=True)

df_final.to_csv("data/voies_echant_ban_2.csv", index=False)

# retravailler les rejected

df_retravaille = pd.read_csv("data/voies_echant_ban_2.csv")
df_retravaille.drop(columns=['justification'], inplace=True)
df_retravaille.to_csv("data/voies_echant_ban_2.csv", index=False)

