# -*- coding: utf-8 -*-
import logging
import sys
import pandas as pd
import os

from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher


def run():
    logging.info("Programme de découpage des libellés de voies")
    format_data = sys.argv[1]

    if format_data == "parquet":
        filename_majic_parquet = sys.argv[2]

        print("Lecture du fichier en entrée")
        voies_data_df = pd.read_parquet("../data/" + filename_majic_parquet + ".parquet.gz")

        voies_data = voies_data_df["dvoilib"].values.tolist()

    elif format_data == "label":
        voie_label = sys.argv[2]
        voies_data = [voie_label.upper()]

    voies_data = list(set(voies_data))

    typevoiedetector: TypeVoieDecoupageLauncher = TypeVoieDecoupageLauncher()
    voies_processed = typevoiedetector.execute(voies_data=voies_data)

    if format_data == "parquet":
        print("Enregistrement des voies traitées")
        result_file_name = sys.argv[3]

        voies_processed_list = [[voie.label_raw, voie.num_assigned, voie.type_assigned, voie.label_assigned, voie.compl_assigned] for voie in voies_processed]

        voies_processed_df = pd.DataFrame(voies_processed_list, columns=["libelle_origin", "numero", "type", "libelle_voie", "complement"])

        result_filepath = os.path.abspath("../data/" + result_file_name + ".parquet.gz")
        voies_processed_df.to_parquet(result_filepath)

        print(
            "Les voies traitées ont été enregistrées et sont accessibles en cliquant + Ctrl \
sur ce lien :"
        )
        print(f"\033]8;;file://{result_filepath}\033\\{result_filepath}\033]8;;\033\\")

    elif format_data == "label":
        voie = voies_processed[0]
        print(" ")
        print("*** Résultat ***")
        print(" ")
        print(f"Nom de voie non traitée: {voie.label_raw}")
        print(f"Type de voie: {voie.type_assigned}")
        print(f"Nom de voie: {voie.label_assigned}")
        print(f"Complément d'adresse: {voie.compl_assigned}")
        print(" ")
        print("*********")


if __name__ == "__main__":
    run()
