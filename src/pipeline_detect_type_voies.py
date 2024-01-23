import pandas as pd
import sys

from voie_classes.voie import Voie
from voie_classes.decoupage_voie import DecoupageVoie

from preprocessors.type_voie_majic_preprocessor import TypeVoieMajicPreprocessor
from preprocessors.voie_data_preprocessor import VoieDataPreprocessor
from utils.proc_utils import save_voies_processed
from processors.no_type.no_type_voies_handler import NoTypeVoiesHandler
from processors.one_type.one_type_voies_handler import OneTypeVoiesHandler
from processors.two_types.two_types_voies_handler import TwoTypesVoiesHandler
from processors.three_more_types.three_more_types_voies_handler import ThreeMoreTypesVoiesHandler


class TypeVoieDetector:
    def __init__(self,
                 voies_data: list,
                 ):

        self.voies_data = voies_data
        self.type_voie_df = None
        self.code2lib = None
        self.voies_preproc = None
        self.voies_proc = None

    def preprocess_type_voie(self):
        self.type_voie_df, self.code2lib = TypeVoieMajicPreprocessor().run()

    def preprocess_voie_libelle(self):
        voies_objects = [Voie(elt) for elt in self.voies_data]
        self.voies_preproc = VoieDataPreprocessor(voies_objects,
                                                  self.type_voie_df,
                                                  self.code2lib).run()

    def instantiate_processing(self):
        self.voies_preproc = [DecoupageVoie(
                              voie.label_raw,
                              voie.infolib) for voie in self.voies_preproc]

    def run_processing_voies(self):

        print('Processing des voies sans type détecté')
        voies_proc_0 = NoTypeVoiesHandler(self.voies_preproc).run()
        self.voies_proc = voies_proc_0
        print("Done")

        print('Processing des voies avec un type détecté')
        voies_proc_1 = OneTypeVoiesHandler(self.voies_preproc).run()
        self.voies_proc += voies_proc_1
        print("Done")

        # print('Processing des voies avec deux types détectés')
        # voies_proc_2 = TwoTypesVoiesHandler(self.voies_preproc).run()
        # self.voies_proc += voies_proc_2
        # print("Done")

        # print('Processing des voies avec trois types détectés ou plus')
        # voies_proc_3_more = ThreeMoreTypesVoiesHandler(self.voies_preproc).run()
        # self.voies_proc += voies_proc_3_more
        # print("Done")

    def run(self):

        print("*********")
        print(' ')
        print('Preprocessing')
        print(' ')
        print("*********")

        print("Preprocessing des données 'types de voie' issues de Majic")
        self.preprocess_type_voie()
        print("Done")

        print("Preprocessing des libellés de voie donnés en entrée")
        self.preprocess_voie_libelle()
        print("Done")

        print('Preprocessing fini')

        print("*********")
        print(' ')
        print('Processing')
        print(' ')
        print("*********")

        self.instantiate_processing()

        self.run_processing_voies()
        print('Processing fini')

        # return self.voies_proc
        return self.voies_preproc


if __name__ == "__main__":
    print('Lancement du pipeline pour découper correctement un libellé de voie en \
type/libellé/complément')
    format_data = sys.argv[1]

    if format_data == "parquet":
        filename_majic_parquet = sys.argv[2]

        print('Lecture du fichier en entrée')
        voies_data_df = pd.read_parquet("../data/" + filename_majic_parquet + ".parquet.gz")

        voies_data = voies_data_df['dvoilib'].values.tolist()

    elif format_data == "label":
        voie_label = sys.argv[2]
        voies_data = [voie_label.upper()]

    voies_data = list(set(voies_data))

    voies_processed = TypeVoieDetector(voies_data).run()

    if format_data == "parquet":
        print('Enregistrement des voies traitées')
        result_file_name = sys.argv[3]
        result_filepath = save_voies_processed(voies_processed, result_file_name)

        print("Les voies traitées ont été enregistrées et sont accessibles en cliquant + Ctrl \
sur ce lien :")
        print(f"\033]8;;file://{result_filepath}\033\\{result_filepath}\033]8;;\033\\")

    elif format_data == "label":
        voie = voies_processed[0]
        print(' ')
        print("*** Résultat ***")
        print(' ')
        print(f"Nom de voie non traitée: {voie.label_raw}")
        print(f"Nom de voie traitée: {voie.infolib.label_preproc}")
        print(f"Type(s) détecté(s): {voie.infolib.types_and_positions}")
        # print(f"Postagging : {voie.infolib.label_postag}")
        # print(f"Numéro: {voie.num_assigned}")
        print(f"Type de voie: {voie.type_assigned}")
        print(f"Nom de voie: {voie.label_assigned}")
        print(f"Complément d'adresse: {voie.compl_assigned}")
        print(' ')
        print("*********")

# python pipeline_detect_type_voies.py "label" "IMM ERNEST RENAN RUE DES LYS"
# python pipeline_detect_type_voies.py "parquet" "majic_2021" "essai"
