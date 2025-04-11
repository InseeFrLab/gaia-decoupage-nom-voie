import pandas as pd
import numpy as np

# sortir les tables de DBEAVER

# SELECT h.nom_voie, h.type_voie_parse, h.libelle_voie_parse, h.complement_adresse  
# FROM public.historique_chargements_ban h
# WHERE h.id_chargement = 195
# ORDER BY RANDOM()
# LIMIT 5000;


# SELECT h.dvoilib, h.type_voie_parse, h.libelle_voie_parse, h.complement_adresse  
# FROM public.historique_chargements_majic h
# WHERE h.id_chargement = 7
# ORDER BY RANDOM()
# LIMIT 5000;


# SELECT h.denomination_de_voie_type, h.denomination_de_voie_libelle, h.type_voie_parse, h.libelle_voie_parse, h.complement_adresse  
# FROM public.historique_chargements_rca h
# WHERE h.id_chargement = 206
# ORDER BY RANDOM()
# LIMIT 5000;

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

i = 1
df = pd.read_json(f"C:/Users/FI7L7T/Documents/gaia/echant_voies/voies_echant_{source}_{i}.json")
df.drop(columns=['count'], inplace=True)

col_names_1 = ['nom_voie_norm_query', 'id_type_voie_match1', 'nom_voie_norm_match1', 'complement_adresse_match1', 'justification']
new_col_names_1 = {'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match1': 'id_type_voie', 'nom_voie_norm_match1': 'nom_voie_norm', 'complement_adresse_match1': 'complement_adresse'}

col_names_2 = ['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']
new_col_names_2 = {'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'}

if source == 'rca':
    df['nom_voie_norm_query'] = df['id_type_voie_query'] + ' ' + df['nom_voie_norm_query']

df_both = df[df['similarity'] == 'Both accepted'][col_names_2]
df_both = df_both.rename(columns=new_col_names_2)

df_acc1 = df[df['similarity'] == 'Accepted 1'][col_names_1]
df_acc1 = df_acc1.rename(columns=new_col_names_1)

df_acc2 = df[df['similarity'] == 'Accepted 2'][col_names_2]
df_acc2 = df_acc2.rename(columns=new_col_names_2)

df_rej = df[df['similarity'] == 'Rejected'][col_names_2]
df_rej = df_rej.rename(columns=new_col_names_2)

df_indecis = df[df['similarity'] == 'Undecided'][col_names_2]
df_indecis = df_indecis.rename(columns=new_col_names_2)

df_final = pd.concat([df_both, df_acc1, df_acc2, df_rej, df_indecis], ignore_index=True)

df_final.to_csv(f"C:/Users/FI7L7T/Documents/gaia/echant_voies/voies_echant_{source}_{i}_to_remake.csv", index=False)

# retravailler les rejected

df_retravaille = pd.read_csv(f"C:/Users/FI7L7T/Documents/gaia/echant_voies/voies_echant_{source}_{i}_to_remake.csv")
df_retravaille.drop(columns=['justification'], inplace=True)
df_retravaille.to_csv(f"C:/Users/FI7L7T/Documents/gaia/echant_voies/voies_echant_{source}_{i}_done.csv", index=False)

