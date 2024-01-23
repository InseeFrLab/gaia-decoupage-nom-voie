import pandas as pd

from constants.constant_dicts import (new_lib_for_existing_codes,
                                      new_codes,
                                      other_spelling_for_codes)
from constants.constant_lists import (unique_libs_for_codes, other_libs_for_codes)


class TypeVoieMajicPreprocessor:
    def __init__(self):
        self.type_voie_df = pd.read_csv("../data/type_voie_majic.csv")

    def enrich_reduced_lib(self):
        """
        Enrichit les codes qui ont aussi un code comme libellé dans
        le DataFrame.

        Cette méthode remplace les libellés existants dans la colonne 'LIBELLE'
        du DataFrame 'type_voie_df' par de nouveaux libellés spécifiés dans le
        dictionnaire 'new_lib_for_existing_codes'. Cela est utile pour
        remplacer les abréviations par des formes complètes.

        """
        self.type_voie_df['LIBELLE'] = self.type_voie_df['LIBELLE'].replace(new_lib_for_existing_codes)

    def choose_unique_lib(self):
        """
        Sélectionne un libellé unique pour les codes de type de voie qui en
        ont plusieurs.

        Cette méthode traite les cas où un même code de type de voie a
        plusieurs libellés associés, séparés par des barres '|'. Elle permet
        de choisir un libellé unique par code.

        La méthode extrait d'abord les libellés contenant des barres '|',
        les divise en libellés séparés,  puis réintègre une sélection de ces
        nouveaux libellés dans le DataFrame principal 'type_voie_df'.
        Les indices spécifiques [0, 2, 4, 7] sont utilisés pour choisir les
        libellés à conserver.

        Retourne :
            DataFrame contenant les libellés non conservés pour chaque code.
        """
        list_barre = [elt for elt in self.type_voie_df['LIBELLE'].tolist() if '|' in elt]
        libs_for_code_df = self.type_voie_df[self.type_voie_df['LIBELLE'].isin(list_barre)]

        indices_a_supprimer = libs_for_code_df.index
        self.type_voie_df = self.type_voie_df.drop(indices_a_supprimer)

        libs_for_code_df = libs_for_code_df.assign(LIBELLE=libs_for_code_df['LIBELLE'].str.split('|')
                                                   ).explode('LIBELLE'
                                                             ).reset_index(drop=True)

        unique_libs_for_codes_df = libs_for_code_df[libs_for_code_df['LIBELLE'].isin(unique_libs_for_codes)]
        self.type_voie_df = pd.concat([self.type_voie_df,
                                       unique_libs_for_codes_df],
                                      ignore_index=True)
        return libs_for_code_df

    def new_codes_lib(self):
        """
        Ajoute un nouveau code de type de voie au DataFrame.

        Cette méthode crée une nouvelle ligne dans le DataFrame 'type_voie_df'
        pour un code de type de voie qui n'était pas présent dans les données
        originales. Le nouveau code et son libellé correspondant sont définis
        dans le dictionnaire 'new_codes'.

        Après l'ajout, le DataFrame est trié par le code de type de voie pour
        maintenir l'ordre, et l'index est réinitialisé pour une meilleure
        cohérence.
        """
        new_row_df = pd.DataFrame(new_codes)
        self.type_voie_df = pd.concat([self.type_voie_df, new_row_df],
                                      ignore_index=True
                                      ).sort_values(by='CODE'
                                                    ).reset_index(drop=True)

    def create_dict_code_lib(self):
        """
        Crée un dictionnaire à partir du DataFrame en mappant les codes de
        type de voie à leurs libellés uniques.

        Cette méthode transforme le DataFrame 'type_voie_df', en un
        dictionnaire où chaque code de type de voie (CODE) est mappé à un
        libellé unique (LIBELLE).

        Retourne :
            Un dictionnaire avec les codes de type de voie comme clés
            et les libellés correspondants comme valeurs.
        """
        return self.type_voie_df.set_index('CODE')['LIBELLE'].to_dict()

    def new_spellings_for_code(self,
                               libs_for_code_df: pd.DataFrame):
        """
        Ajoute de nouvelles orthographes pour les codes de types de voie.

        Cette méthode enrichit le DataFrame 'type_voie_df' avec des
        orthographes alternatives pour les libellés de types de voie.
        Elle prend un DataFrame 'libs_for_code_df' contenant des libellés
        alternatifs et les intègre dans le DataFrame principal. Ensuite,
        elle ajoute d'autres orthographes spécifiées dans
        'other_spelling_for_codes'.

        Les nouvelles entrées sont triées par code et l'index du DataFrame est
        réinitialisé pour garantir la cohérence.

        Paramètres :
        - libs_for_code_df : DataFrame contenant les libellés alternatifs
                             à ajouter.
        """
        other_libs_for_codes_df = libs_for_code_df[libs_for_code_df['LIBELLE'].isin(other_libs_for_codes)]
        self.type_voie_df = pd.concat([self.type_voie_df,
                                       other_libs_for_codes_df],
                                      ignore_index=True)
        new_row_df = pd.DataFrame(other_spelling_for_codes)

        self.type_voie_df = pd.concat([self.type_voie_df, new_row_df],
                                      ignore_index=True
                                      ).sort_values(by='CODE',
                                                    ascending=True
                                                    ).reset_index(drop=True)

    def run(self):
        """
        Nettoie et enrichit les données de type de voie.

        Cette méthode exécute une série d'opérations de nettoyage et
        d'enrichissement sur le DataFrame 'type_voie_df', qui contient
        les codes et libellés des types de voie. Elle commence par
        sélectionner un libellé unique pour chaque code,
        ajoute de nouveaux codes non présents dans les données initiales,
        crée un dictionnaire mappant les codes aux libellés,
        et ajoute différentes orthographes pour les codes.

        Retourne : Le DataFrame nettoyé et un dictionnaire des codes
        avec libellés uniques.
        """
        self.enrich_reduced_lib()
        libs_for_code_df = self.choose_unique_lib()
        self.new_codes_lib()
        code2lib = self.create_dict_code_lib()
        self.new_spellings_for_code(libs_for_code_df)

        return self.type_voie_df, code2lib
