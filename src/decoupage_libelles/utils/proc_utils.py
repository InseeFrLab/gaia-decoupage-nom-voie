from typing import List
import pandas as pd
import os

from voie_classes.decoupage_voie import DecoupageVoie


def save_voies_processed(voies_processed: List[DecoupageVoie], file_name):
    voies_processed_list = [[voie.label_raw,
                             voie.num_assigned,
                             voie.type_assigned,
                             voie.label_assigned,
                             voie.compl_assigned] for voie in voies_processed]

    voies_processed_df = pd.DataFrame(voies_processed_list,
                                      columns=['libelle_origin',
                                               'numero',
                                               'type',
                                               'libelle_voie',
                                               'complement'])

    result_filepath = os.path.abspath("../data/" + file_name + ".parquet.gz")
    voies_processed_df.to_parquet(result_filepath)

    return result_filepath
