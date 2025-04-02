import pandas as pd

df = pd.read_json("data/echant_voies_1k.json")
df.drop(columns=['count'], inplace=True)

df_both = df[df['similarity'] == 'Both accepted'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_both = df_both.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_acc1 = df[df['similarity'] == 'Accepted 1'][['nom_voie_norm_query', 'id_type_voie_match1', 'nom_voie_norm_match1', 'complement_adresse_match1', 'justification']]
df_acc1 = df_acc1.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match1': 'id_type_voie', 'nom_voie_norm_match1': 'nom_voie_norm', 'complement_adresse_match1': 'complement_adresse'})

df_acc2 = df[df['similarity'] == 'Accepted 2'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_acc2 = df_acc2.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_rej = df[df['similarity'] == 'Rejected'][['nom_voie_norm_query', 'id_type_voie_match2', 'nom_voie_norm_match2', 'complement_adresse_match2', 'justification']]
df_rej = df_rej.rename(columns={'nom_voie_norm_query': 'nom_voie', 'id_type_voie_match2': 'id_type_voie', 'nom_voie_norm_match2': 'nom_voie_norm', 'complement_adresse_match2': 'complement_adresse'})

df_final = pd.concat([df_both, df_acc1, df_acc2, df_rej], ignore_index=True)

df_final.to_csv("data/echant_voies_1k.csv", index=False)

# retravailler les rejected

df_retravaille = pd.read_csv("data/echant_voies_1k.csv")
df_retravaille.drop(columns=['justification'], inplace=True)
df_retravaille.to_csv("data/echant_voies_1k.csv", index=False)

