# -*- coding: utf-8 -*-
import logging
import sys
import pandas as pd
import os

from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher


def run():
    logging.info("Programme de découpage des libellés de voies")
    format_data = sys.argv[1]

    if format_data == "parquetgz" or format_data == "parquet":
        filename_parquet = sys.argv[2]

        logging.info("Lecture du fichier en entrée")
        if format_data == "parquetgz":
            voies_data_df = pd.read_parquet("../data/" + filename_parquet + ".parquet.gz")
        elif format_data == "parquet":
            voies_data_df = pd.read_parquet("../data/" + filename_parquet + ".parquet")

        var_name_voie = sys.argv[3]
        voies_data = voies_data_df[var_name_voie].values.tolist()

    elif format_data == "label":
        voie_label = sys.argv[2]
        voies_data = [voie_label]

    voies_data = list(set(voies_data))

    typevoiedecoupagelauncher: TypeVoieDecoupageLauncher = TypeVoieDecoupageLauncher()
    voies_processed = typevoiedecoupagelauncher.execute(voies_data=voies_data)

    if format_data == "parquetgz" or format_data == "parquet":
        logging.info("Enregistrement des voies traitées")
        result_file_name = sys.argv[4]

        voies_processed_list = [
            [voie.label_origin.lower(), voie.num_assigned, voie.indice_rep.lower(), voie.type_assigned.lower(), voie.label_assigned.lower(), voie.compl_assigned.lower()] for voie in voies_processed
        ]

        voies_processed_df = pd.DataFrame(voies_processed_list, columns=[var_name_voie, "numero", "indice_rep", "type", "libelle_voie", "complement"])
        resultat_df = pd.merge(voies_data_df, voies_processed_df, left_on=var_name_voie, right_on=var_name_voie, how="left")

        result_filepath = os.path.abspath("../data/" + result_file_name + ".parquet")
        resultat_df.to_parquet(result_filepath)

        logging.info("Les voies traitées ont été enregistrées et sont accessibles en cliquant + Ctrl sur ce lien :")
        logging.info(f"\033]8;;file://{result_filepath}\033\\{result_filepath}\033]8;;\033\\")

    elif format_data == "label":
        voie = voies_processed[0]
        print(" ")
        logging.info("*** Résultat ***")
        print(" ")
        print(f"Nom de voie non traitée: {voie.label_origin}")
        print(f"Type de voie: {voie.type_assigned}")
        print(f"Nom de voie: {voie.label_assigned}")
        print(f"Complément d'adresse: {voie.compl_assigned}")
        print(" ")
        print("*********")


if __name__ == "__main__":
    run()
